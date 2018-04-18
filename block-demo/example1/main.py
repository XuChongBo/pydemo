import argparse
import os
import shutil
import time
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torch
import random
from PIL import Image
import sys
import os
import torchvision
import torch.nn as nn
import dataset 
from torch.autograd import Variable
import utils
import config
from model import SRGAN


def main():
    config.printDetail()
    raw_input("press anykey ")
    if config.evaluate and not config.snapshot:
        print("ERROR: need a snapshot to evalute.")
        sys.exit(1)

    if config.snapshot and not os.path.isfile(config.snapshot):
        print("ERROR: no snapshot found at '{}' ".format(config.snapshot))
        sys.exit(1)

    if config.GPU_ID is not None:
        print("use cuda")
        cudnn.benchmark = True
        torch.cuda.set_device(config.GPU_ID)

    utils.plotText()
    print("create model...")
    model = SRGAN(gpu_id=config.GPU_ID)
    start_epoch = 1  # epoch start from 1 
    # optionally resume from a checkpoint
    if config.snapshot:
        print("=> loading check_oint '{}'".format(config.snapshot))
        checkpoint = torch.load(config.snapshot)
        start_epoch = checkpoint['epoch']
        model.loadDict(checkpoint)
        print("=> loaded checkpoint '{}' (epoch {})" .format(config.snapshot, checkpoint['epoch']))

    if config.evaluate:
        print( "only evaluate it")
        valid_dataset = dataset.Dataset(desc_file_path='valid.txt')
        valid_loader = torch.utils.data.DataLoader(dataset=valid_dataset, batch_size=config.batch_size, shuffle=False, num_workers=2)
        gan_loss, content_loss = validate(valid_loader, model)
        print ("gan_loss:", gan_loss, "content_loss:",content_loss)
    else:
        # prepare dirs
        print ("prepare dirs and links")
        utils.prepareDirs()
        # Datasets
        print ("init data loader...")
        train_dataset = dataset.Dataset(desc_file_path='train-data.txt')
        train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=config.batch_size, shuffle=True, num_workers=2)
        valid_dataset = dataset.Dataset(desc_file_path='valid-data.txt')
        valid_loader = torch.utils.data.DataLoader(dataset=valid_dataset, batch_size=config.batch_size, shuffle=False, num_workers=2)

        print( "begin train..")
        for epoch in range(start_epoch, config.epochs+1):   
            #adjust_learning_rate(optimizer, epoch)
            # train for one epoch
            train(epoch,  train_loader, model)
            # evaluate on validation set
            gan_loss, content_loss = validate(valid_loader, model)
            # test eyes
            """
            test(model, "age2687.jpg.png", epoch)
            test(model, "small_left_eye.png", epoch)
            test(model, "32.png", epoch)
            """
            # test face 
            test(model, "44.png", epoch)
            test(model, "36.png", epoch)

            print ('validation  gan_loss: %.4f, content_loss: %.4f' %(gan_loss, content_loss))
            if (epoch) % config.plot_freq_epoch  == 0:
                utils.plot('loss', 'valid-gan-loss', epoch, gan_loss)
                utils.plot('loss', 'valid-content-loss', epoch, content_loss)

def train(epoch,  train_loader, model ):
    # switch to train mode
    iters = len(train_loader)
    for i, (lr_imgs, hr_imgs) in enumerate(train_loader):
        lr_imgs = lr_imgs.cuda()
        hr_imgs = hr_imgs.cuda()
        lr_imgs = Variable(lr_imgs)
        hr_imgs = Variable(hr_imgs)

        #print lr_imgs.size()
        #print hr_imgs.size()

        real_labels = Variable(torch.ones(lr_imgs.size(0)).cuda())
        fake_labels = Variable(torch.zeros(lr_imgs.size(0)).cuda())

        sr_imgs, d_loss,d_real,d_fake,d_fake2, gan_loss, content_loss = model.fit(lr_imgs, hr_imgs, update=True)

        if (i+1) % config.print_freq_iter == 0:
            print('[INFO] [%s] Epoch [%d/%d], Step[%d/%d], bathsize[%d], '
                    'oldD-d_loss: %.4f,'
                    'oldD-D(x):%.2f, oldD-D(G(z)): %.2f, '
                    'newD-D(G(z)): %.2f ' 
                    'newD-gan_loss: %.4f, ' 
                    'newD-content_loss: %.4f, ' 
                  %(config.experiment_name, epoch, config.epochs, i+1, iters, config.batch_size, 
                      d_loss.data[0], 
                      d_real.data.min(), d_fake.data.max(),
                      d_fake2.data.mean(),
                      gan_loss.data[0],
                      content_loss.data[0]))

    if (epoch) % config.plot_freq_epoch  == 0:
        utils.plot('D(x)', 'oldD-D(x)', epoch, d_real.data.mean())
        utils.plot('D(x)', 'oldD-D(G(z))', epoch, d_fake.data.mean())
        utils.plot('D(x)', 'newD-D(G(z))', epoch, d_fake2.data.mean())
        utils.plot('loss', 'oldD-d_loss', epoch, d_loss.data[0])
        utils.plot('loss', 'newD-gan_loss', epoch, gan_loss.data[0])
        utils.plot('loss', 'newD-content_loss', epoch, content_loss.data[0])
        # Save the sampled images
        k = random.randint(0,lr_imgs.size(0)-1)
        utils.save_image(lr_imgs.data[k], os.path.join(config.LR_FOLDER,'lr_%d_%d.png' %(epoch, k)) )
        utils.save_image(hr_imgs.data[k], os.path.join(config.HR_FOLDER,'hr_%d_%d.png' %(epoch, k)) )
        utils.save_image(sr_imgs.data[k], os.path.join(config.SR_FOLDER,'sr_%d_%d.png' %(epoch, k)) )


    if (epoch) % config.snapshot_freq_epoch == 0:
        # Save the Models
        state = model.stateDict()
        state['epoch']= epoch
        torch.save(state, os.path.join(config.MODEL_FOLDER,'snapshot_%d.pkl' %(epoch)) ) 
#torch.save(generator.state_dict(), os.path.join(MODEL_FOLDER,'generator_%d.pkl' %(epoch)) ) 




def validate(valid_loader, model):
    total_gan_loss = 0
    total_content_loss = 0
    total = 0
    for i, (lr_imgs, hr_imgs) in enumerate(valid_loader):
        lr_imgs = lr_imgs.cuda()
        hr_imgs = hr_imgs.cuda()
        lr_imgs = Variable(lr_imgs)
        hr_imgs = Variable(hr_imgs)
        gan_loss, content_loss = model.fit(lr_imgs, hr_imgs, update=False)
        total_gan_loss += gan_loss.data[0]
        total_content_loss += content_loss.data[0]
        total += 1
    return total_gan_loss/total,  total_content_loss/total


def test(model, img_path, epoch):
    g = model.G
    g.eval()
    #self.model_g.eval()
    trans = transforms.Compose([transforms.ToTensor(), ])
    # inference
    img = Image.open(img_path)
    lr_img = trans(img)
    lr_imgs = lr_img.view(1, lr_img.size(0), lr_img.size(1), lr_img.size(2))
    print( "inference..")
    lr_imgs = Variable(lr_imgs,volatile=True)
    sr_imgs = g(lr_imgs.cuda())
    utils.save_image(sr_imgs.data[0], os.path.join(config.PEEK_FOLDER, os.path.basename(img_path)+'_%d.png' % epoch ) )


        
if __name__ == '__main__':
    main()
