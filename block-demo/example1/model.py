#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torch
import math
import torchvision
import torch.nn as nn
import torchvision.datasets as dsets
import dataset 
from torch.autograd import Variable
from D import Discriminator
from G import  Generator
import utils
import config
from vgg import VGG19Feature


class SRGAN:
    def __init__(self, gpu_id):

        #vgg_feature = torchvision.models.vgg19()
        self.vgg_feature = VGG19Feature()
        self.avg_pool2d = nn.AvgPool2d(2, stride=2)
        # create model
        print "create model and optimizers . .."
        self.D = Discriminator()
        print self.D
        raw_input("press any key")
        self.G = Generator()
        if config.GAN_SETTING == "WGAN":
            self.D_optimizer = torch.optim.RMSprop(self.D.parameters(), lr=5e-5)
            self.G_optimizer = torch.optim.RMSprop(self.G.parameters(), lr=5e-5)
        elif 0:
            self.D_optimizer = torch.optim.SGD(self.D.parameters(), lr=1e-5)
            self.G_optimizer = torch.optim.SGD(self.G.parameters(), lr=1e-5)
        else:
            #self.D_optimizer = torch.optim.Adam(D.parameters(), lr=10e-5,  betas=(0.5, 0.999))
            self.D_optimizer = torch.optim.RMSprop(self.D.parameters(), lr=5e-5)
            self.G_optimizer = torch.optim.Adam(self.G.parameters(), lr=5e-5)

        # Loss and Optimizer
        self.bce_loss = nn.BCELoss()
        self.mse_loss= nn.MSELoss()

        if gpu_id is not None:
            print "send model to gpu.."
            self.D.cuda()
            self.G.cuda()
            self.bce_loss.cuda()
            self.mse_loss.cuda()
            self.vgg_feature.cuda()
        print "send model to gpu done."

    def loadDict(self, state):
        self.D.load_state_dict(state['D_model'])
        self.D_optimizer.load_state_dict(state['D_optimizer'])
        self.G.load_state_dict(state['G_model'])
        self.G_optimizer.load_state_dict(state['G_optimizer'])

    def contentLossG(self, lr_imgs, sr_imgs, hr_imgs):
        if config.CONTENT_LOSS_TYPE == 'VGG':
            sr_embedding = self.vgg_feature(sr_imgs)
            hr_embedding = self.vgg_feature(hr_imgs)
            loss = self.mse_loss(sr_embedding, hr_embedding.detach())
        elif config.CONTENT_LOSS_TYPE == 'LR':
            loss = self.mse_loss(sr_imgs, hr_imgs)
            loss += self.mse_loss(self.avg_pool2d(sr_imgs), lr_imgs)
        else:
            loss = self.mse_loss(sr_imgs, hr_imgs)
        return loss

    def ganLossG(self, d_fake):
        if config.GAN_SETTING == "WGAN":
            loss = -torch.mean(d_fake)
        elif config.GAN_SETTING == "LSGAN":
            loss = 0.5 * torch.mean((d_fake - 1)**2)
        else:
            real_labels = Variable(torch.ones(d_fake.size(0)).cuda())
            fake_labels = Variable(torch.zeros(d_fake.size(0)).cuda())
            loss = self.bce_loss(d_fake, real_labels)
        return loss

    def lossD(self, d_real, d_fake):
        if config.GAN_SETTING == "WGAN":
            loss = -(torch.mean(d_real) - torch.mean(d_fake))
        elif config.GAN_SETTING == "LSGAN":
            loss = 0.5 * (torch.mean((d_real - 1)**2) + torch.mean(d_fake**2))
        else:
            real_labels = Variable(torch.ones(d_real.size(0)).cuda())
            fake_labels = Variable(torch.zeros(d_fake.size(0)).cuda())
            real_loss = self.bce_loss(d_real, real_labels)
            fake_loss = self.bce_loss(d_fake, fake_labels)
            # -- loss and update 
            loss = real_loss + fake_loss
        return loss


    def fit(self, lr_imgs, hr_imgs, update=True):
        if not update:
            self.D.eval()
            self.G.eval()
            sr_imgs = self.G(lr_imgs)
            d_fake2 = self.D(sr_imgs)
            gan_loss = self.ganLossG(d_fake2)
            content_loss = self.contentLossG(lr_imgs, sr_imgs, hr_imgs)
            return gan_loss, content_loss
        else:
            self.D.train()
            self.G.train()
            # ============= Train the D  ====================
            self.D.zero_grad()
            d_real = self.D(hr_imgs)
            
            sr_imgs = self.G(lr_imgs)
            d_fake = self.D(sr_imgs.detach()) 
#            print "after d fake"
#utils.printGPUINFO()
            d_loss = self.lossD(d_real, d_fake)
#            print "after lossd"
#            utils.printGPUINFO()
            d_loss.backward()
            self.D_optimizer.step()
            if config.GAN_SETTING == "WGAN":
                for p in self.D.parameters():
                    p.data.clamp_(-0.01, 0.01)

            for k in range(1):
                #============== Train the G 
                self.G.zero_grad()
                sr_imgs = self.G(lr_imgs)
                #print 'fake size', sr_imgs.size()
                d_fake2 = self.D(sr_imgs)
                content_loss = self.contentLossG(lr_imgs, sr_imgs, hr_imgs)
                if config.GAN_LOSS_FACTOR > 0:
                    gan_loss = self.ganLossG(d_fake2)
                    g_loss = config.GAN_LOSS_FACTOR*gan_loss + content_loss
                else:
                    gan_loss = Variable(torch.zeros(1))
                    g_loss = content_loss
                g_loss.backward()
                self.G_optimizer.step()

            return sr_imgs, d_loss,d_real,d_fake,d_fake2, gan_loss, content_loss

    def stateDict(self):
        state = {
                'D_model': self.D.state_dict(),
                'D_optimizer': self.D_optimizer.state_dict(),
                'G_model': self.G.state_dict(),
                'G_optimizer': self.G_optimizer.state_dict(),
        }
        return state

