from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *

client = RecombeeClient('university-of-jordan-dev', 'sMGOTwMPzOPM3l6Tmxs8jXZ2WeCskPR9dnzKrdBczJHy1vdRFQs9HldcLPC8W63N')

result = client.send(ListItems(filter="\'Brand\'== \"Gap\""))



item_img = {
    'item_99': 'https://www.gap.com/webcontent/0018/101/739/cn18101739.jpg',
    'item_98': 'https://www.gap.com/webcontent/0017/029/794/cn17029794.jpg',
    'item_97': 'https://www.gap.com/webcontent/0017/341/330/cn17341330.jpg',
    'item_96': 'https://www.gap.com/webcontent/0018/052/667/cn18052667.jpg', #is actually grey
    'item_95': 'https://www.gap.com/webcontent/0018/306/804/cn18306804.jpg',
    'item_94': 'https://www.gap.com/webcontent/0017/341/309/cn17341309.jpg',
    'item_93': 'https://www.gap.com/webcontent/0017/667/434/cn17667434.jpg',
    'item_92': 'https://www.gap.com/webcontent/0017/629/840/cn17629840.jpg',
    'item_91': 'https://www.gap.com/webcontent/0017/818/317/cn17818317.jpg',
    'item_90': 'https://www.gap.com/webcontent/0017/331/404/cn17331404.jpg',
    'item_89': 'https://www.gap.com/webcontent/0018/191/012/cn18191012.jpg',
    'item_88': 'https://www.gap.com/webcontent/0018/084/015/cn18084015.jpg',#item_87 sold out
    'item_86': 'https://www.gap.com/webcontent/0017/667/550/cn17667550.jpg',
    'item_85': 'https://www.gap.com/webcontent/0015/161/274/cn15161274.jpg',
    'item_84': 'https://www.gap.com/webcontent/0018/032/751/cn18032751.jpg',
    'item_83': 'https://www.gap.com/webcontent/0018/028/587/cn18028587.jpg',
    'item_82': 'https://www.gap.com/webcontent/0018/028/638/cn18028638.jpg',
    'item_81': 'https://www.gap.com/webcontent/0018/216/814/cn18216814.jpg',
    'item_80': 'https://www.gap.com/webcontent/0017/854/786/cn17854786.jpg',
    'item_79': 'https://www.gap.com/webcontent/0017/160/907/cn17160907.jpg',
    'item_78': 'https://www.gap.com/webcontent/0017/854/831/cn17854831.jpg',#item 77 dne
    'item_76': 'https://www.gap.com/webcontent/0017/732/977/cn17732977.jpg',#item 75 and 74 dne
    'item_73': 'https://www.gap.com/webcontent/0017/616/917/cn17616917.jpg',#item72 dne
    'item_71': 'https://www.gap.com/webcontent/0017/616/934/cn17616934.jpg',#item70 dne
    'item_69': 'https://www.gap.com/webcontent/0014/773/672/cn14773672.jpg',
    'item_68': 'https://www.gap.com/webcontent/0014/782/436/cn14782436.jpg',#item 67 dne
    'item_66': 'https://www.gap.com/webcontent/0015/840/121/cn15840121.jpg',
    'item_65': 'https://www.gap.com/webcontent/0017/365/593/cn17365593.jpg',
    'item_64': 'https://www.gap.com/webcontent/0017/365/559/cn17365559.jpg',
    'item_63': 'https://www.gap.com/webcontent/0015/570/489/cn15570489.jpg',
    'item_62': 'https://www.gap.com/webcontent/0017/880/677/cn17880677.jpg',
    'item_61': 'https://www.gap.com/webcontent/0017/880/689/cn17880689.jpg',
    'item_60': 'https://www.gap.com/webcontent/0017/880/649/cn17880649.jpg',
    'item_59': 'https://www.gap.com/webcontent/0017/851/862/cn17851862.jpg',
    'item_58': 'https://www.gap.com/webcontent/0017/850/257/cn17850257.jpg',#item 57 56 55 dne
    'item_54': 'https://www.gap.com/webcontent/0018/215/735/cn18215735.jpg',
    'item_53': 'https://www.gap.com/webcontent/0018/256/581/cn18256581.jpg',#item title Vintage Soft Henley T-Shirt
    'item_52': 'https://www.gap.com/webcontent/0017/329/690/cn17329690.jpg',
    'item_51': 'https://www.gap.com/webcontent/0017/265/364/cn17265364.jpg',
    'item_50': 'https://www.gap.com/webcontent/0017/265/386/cn17265386.jpg',
    'item_49': 'https://www.gap.com/webcontent/0018/025/935/cn18025935.jpg',
    'item_48': 'https://www.gap.com/webcontent/0017/403/748/cn17403748.jpg',
    'item_47': 'https://www.gap.com/webcontent/0016/669/057/cn16669057.jpg',
    'item_46': 'https://www.gap.com/webcontent/0016/669/083/cn16669083.jpg',#item 45 44 dne
    'item_43': 'https://www.gap.com/webcontent/0018/080/515/cn18080515.jpg',
    'item_42': 'https://www.gap.com/webcontent/0016/391/530/cn16391530.jpg',
    'item_41': 'https://www.gap.com/webcontent/0016/391/509/cn16391509.jpg',
    'item_40': 'https://www.gap.com/webcontent/0017/403/710/cn17403710.jpg',
    'item_198': 'https://www.gap.com/webcontent/0017/793/619/cn17793619.jpg',#item 197 dne
    'item_196': 'https://www.gap.com/webcontent/0017/802/505/cn17802505.jpg',
    'item_195': 'https://www.gap.com/webcontent/0017/835/759/cn17835759.jpg',#item 194  193 192 191 190     dne
    'item_189': 'https://www.gap.com/webcontent/0017/511/626/cn17511626.jpg',
    'item_188': 'https://www.gap.com/webcontent/0016/570/461/cn16570461.jpg',#item 187 dne
    'item_186': 'https://www.gap.com/webcontent/0018/207/353/cn18207353.jpg',#item 185 184 183 182 181dne
    'item_180': 'https://www.gap.com/webcontent/0017/738/782/cn17738782.jpg',#item 179 178 dne
    'item_177': 'https://www.gap.com/webcontent/0017/871/228/cn17871228.jpg',
    'item_176': 'https://www.gap.com/webcontent/0018/091/768/cn18091768.jpg',#item 175
    'item_174': 'https://www.gap.com/webcontent/0018/512/906/cn18512906.jpg',
    'item_173': 'https://www.gap.com/webcontent/0018/178/215/cn18178215.jpg',
    'item_172': 'https://www.gap.com/webcontent/0018/440/158/cn18440158.jpg',#item 161 dne
    'item_160': 'https://www.gap.com/webcontent/0015/595/475/cn15595475.jpg',#item 159 dne
    'item_158': 'https://www.gap.com/webcontent/0017/837/754/cn17837754.jpg',#item 157 156 dne
    'item_155': 'https://www.gap.com/webcontent/0013/989/354/cn13989354.jpg',
    'item_154': 'https://www.gap.com/webcontent/0018/144/576/cn18144576.jpg',
    'item_153': 'https://www.gap.com/webcontent/0018/142/700/cn18142700.jpg',
    'item_152': 'https://www.gap.com/webcontent/0018/187/270/cn18187270.jpg',
    'item_109': 'https://www.gap.com/webcontent/0017/337/371/cn17337371.jpg',
    'item_108': 'https://www.gap.com/webcontent/0017/608/920/cn17608920.jpg',
    'item_107': 'https://www.gap.com/webcontent/0017/752/059/cn17752059.jpg',
    'item_106': 'https://www.gap.com/webcontent/0017/620/407/cn17620407.jpg',
    'item_105': 'https://www.gap.com/webcontent/0017/037/661/cn17037661.jpg',
    'item_104': 'https://www.gap.com/webcontent/0018/052/650/cn18052650.jpg',
    'item_103': 'https://www.gap.com/webcontent/0018/198/342/cn18198342.jpg',
    'item_102': 'https://www.gap.com/webcontent/0017/037/645/cn17037645.jpg',
    'item_101': 'https://www.gap.com/webcontent/0016/458/977/cn16458977.jpg',
    'item_100': 'https://www.gap.com/webcontent/0016/459/714/cn16459714.jpg'
}

requests = []
for key in item_img:
    r = SetItemValues(key, {'Picture': item_img[key]}, cascade_create=True)
    requests.append(r)

br = Batch(requests)
client.send(br)

client.send(SetItemValues('item_96', {'Color': ['Grey']}, cascade_create=True))

"""
client.send(SetItemValues('item_100',
                          {
                              'Picture' : 'https://www.gap.com/webcontent/0016/459/714/cn16459714.jpg'
                          }
                          ,
  cascade_create=True
)
)
"""
