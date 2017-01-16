# coding: utf-8
class CloudSearchResourceList(ListAPIView):
   """
   subject_id:学科id，
   source_type:(1-知识点，2-章节)，
   chapter: * 指定的章节code，后端会自动带上子节点，
   keyword: 关键字，
   order: 0-顺序、1-倒序， 
   cate: * 选择的标签（学案，试卷），
   book：教材版本（”全部“时为空），
   gradecode：年级（”全部“时为空），
   page: 页码(从1开始)
   orderField : 排序字段
   """
   permission_classes = (IsAuthenticated,)
   serializer_class = CloudResourceSerializer
   pagination_class = None

   def get(self, request, *args, **kwargs):
       (stagesubject, sub_cates, source_type, book, gradecode, code, keyword, location, grade, year, order, order_name, order_field, paper_type) = get_params(self)
           if code:
               ids = [code]
           else:
               # 请求的是章节的资源
               if source_type == SOURCE_TYPE.CHAPTER:
                   code_list = get_chapters(book, gradecode, code, stagesubject)
               # 请求的是知识点的资源
               elif source_type == SOURCE_TYPE.KNOWLEDGE:
                   code_list = self.get_knowledges(code, stagesubject)  #获取knowledge codes
               ids = [item['code'].encode('utf8') for item in code_list]

               headers = {'content-type': 'application/x-www-form-urlencoded'}
               url = 'http://' + YCL_HOST + '/v2/resources'
               data = {'subject':stagesubject,'page':self.request.query_params.get('page'),'page_size':self.request.query_params.get('page_size', 15),
                       'section':chapter_ids}
               r = requests.post(url, data=data, headers=headers)
               logger.info("call tiku-ycl service")
               if r.status_code != 200:
                   logger.error("tiku-ycl response: %s" % r.content)
                   raise RuntimeError("call %s error." % url )
               d = r.json()
               #logger.debug("tiku-ycl response: %s" % d)
               count = d['count']
               resource_list = d.get('3',[])+d.get('5',[])
               code_list = [ item['ID'] for item in resource_list ]
               #logger.("code_list %s" % code_list)
               queryset = ExternalResource.objects.filter(code__in=code_list)
               serializer = self.serializer_class(queryset, many=True)
               extra_resources = serializer.data
               logger.info("extra_resources %s" % extra_resources)
               tmp_dict = {}
               for item in extra_resources:
                   tmp_dict[item['code']] = item
               logger.info("tmp_dict %s" % tmp_dict)
               for item in resource_list:
                   tmp =  tmp_dict.get(item['ID'],{})
                   logger.info(tmp)
                   logger.info(item)
                   item.update(tmp)
                   item.pop('ID')
               response = { 'data': {'count':d['count'],'previous':'', 'next':'', 'results':resource_list }, 'code': 1, 'msg': 'ok' }
               #response = { 'data': {'count':10,'previous':'', 'next':'', 'results':[3,4]}, 'code': 1, 'msg': 'ok' }
               logger.info("response %s" % response)
               return Response([response])

       return resources
