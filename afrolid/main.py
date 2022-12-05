# -*- coding: utf-8 -*-
from afrolid import tasks
import argparse
from fairseq import checkpoint_utils, data
import torch
import torch.nn.functional as F
import regex
import sentencepiece as spm


# import math
class classifier():
  def __init__(self, logger, model_path):
    self.logger = logger
    self.model_path = model_path
    self.afrolid_task, self.model, self.tokenizer= self.init_task_model()
    self.lang_info = self.load_langs_info()
    # print(self.lang_info)
  def init_task_model(self):
    # print("dddsssssssss")
    self.logger.info("Initalizing AfroLID's task and model.")
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--task", metavar="TASK", default='afrolid_task',)
    parser.add_argument('-d', "--data", type=str,default=self.model_path)
    args, _ = parser.parse_known_args()
    afrolid_task = tasks.setup_task(args)
    models, _model_args = checkpoint_utils.load_model_ensemble([self.model_path+"/afrolid_v1_checkpoint.pt"], task=afrolid_task)
    model = models[0]
    model.eval()
    tokenizer = spm.SentencePieceProcessor()
    tokenizer.Load(self.model_path+"/afrolid_spm_517_bpe.model")
    return afrolid_task, model, tokenizer
  def load_langs_info(self):
    langs={}
    # df = pd.read_csv(os.path.dirname(__file__)+"/langs_info.tsv", sep='\t')
    # for index, row in df.iterrows():
    #   lang_iso = row['ISO']
    #   lang_name = row['lang_name']
    #   lang_script = row['script']
    #   langs[lang_iso]={'name': lang_name, 'script': lang_script}
    langs={'mda': {'name': 'Mada', 'script': 'Latin'}, 'nin': {'name': 'Ninzo', 'script': 'Latin'}, 'odu': {'name': 'Odual', 'script': 'Latin'}, 'abn': {'name': 'Abua', 'script': 'Latin'}, 'ego': {'name': 'Eggon', 'script': 'Latin'}, 'kyq': {'name': 'Kenga', 'script': 'Latin'}, 'bdh': {'name': 'Baka', 'script': 'Latin'}, 'eka': {'name': 'Ekajuk', 'script': 'Latin'}, 'bza': {'name': 'Bandi', 'script': 'Latin'}, 'bfa': {'name': 'Bari', 'script': 'Latin'}, 'aha': {'name': 'Ahanta', 'script': 'Latin'}, 'box': {'name': 'Bwamu / Buamu', 'script': 'Latin'}, 'wbi': {'name': 'Vwanji', 'script': 'Latin'}, 'mwe': {'name': 'Mwera', 'script': 'Latin'}, 'asa': {'name': 'Asu', 'script': 'Latin'}, 'bem': {'name': 'Bemba / Chibemba', 'script': 'Latin'}, 'beq': {'name': 'Beembe', 'script': 'Latin'}, 'bez': {'name': 'Bena', 'script': 'Latin'}, 'bxk': {'name': 'Bukusu', 'script': 'Latin'}, 'cce': {'name': 'Chopi', 'script': 'Latin'}, 'chw': {'name': 'Chuabo', 'script': 'Latin'}, 'cjk': {'name': 'Chokwe', 'script': 'Latin'}, 'cwe': {'name': 'Kwere', 'script': 'Latin'}, 'dav': {'name': 'Dawida / Taita', 'script': 'Latin'}, 'dhm': {'name': 'Dhimba', 'script': 'Latin'}, 'dig': {'name': 'Chidigo', 'script': 'Latin'}, 'diu': {'name': 'Gciriku', 'script': 'Latin'}, 'dug': {'name': 'Chiduruma', 'script': 'Latin'}, 'ebu': {'name': 'Kiembu / Embu', 'script': 'Latin'}, 'eko': {'name': 'Koti', 'script': 'Latin'}, 'fip': {'name': 'Fipa', 'script': 'Latin'}, 'flr': {'name': 'Fuliiru', 'script': 'Latin'}, 'gog': {'name': 'Gogo', 'script': 'Latin'}, 'guz': {'name': 'Ekegusii', 'script': 'Latin'}, 'gwr': {'name': 'Gwere', 'script': 'Latin'}, 'hay': {'name': 'Haya', 'script': 'Latin'}, 'jit': {'name': 'Jita', 'script': 'Latin'}, 'jmc': {'name': 'Machame', 'script': 'Latin'}, 'kam': {'name': 'Kikamba', 'script': 'Latin'}, 'kck': {'name': 'Kalanga', 'script': 'Latin'}, 'kdc': {'name': 'Kutu', 'script': 'Latin'}, 'kde': {'name': 'Makonde', 'script': 'Latin'}, 'kdn': {'name': 'Kunda', 'script': 'Latin'}, 'kik': {'name': 'Gikuyu / Kikuyu', 'script': 'Latin'}, 'kin': {'name': 'Kinyarwanda', 'script': 'Latin'}, 'kiz': {'name': 'Kisi', 'script': 'Latin'}, 'kki': {'name': 'Kagulu', 'script': 'Latin'}, 'kmb': {'name': 'Kimbundu', 'script': 'Latin'}, 'kng': {'name': 'Kongo', 'script': 'Latin'}, 'koo': {'name': 'Konzo', 'script': 'Latin'}, 'kqn': {'name': 'Kikaonde', 'script': 'Latin'}, 'ksb': {'name': 'Shambala / Kishambala', 'script': 'Latin'}, 'kua': {'name': 'Oshiwambo', 'script': 'Latin'}, 'kuj': {'name': 'Kuria', 'script': 'Latin'}, 'kwn': {'name': 'Kwangali', 'script': 'Latin'}, 'lai': {'name': 'Lambya', 'script': 'Latin'}, 'lam': {'name': 'Lamba', 'script': 'Latin'}, 'lgm': {'name': 'Lega-mwenga', 'script': 'Latin'}, 'lik': {'name': 'Lika', 'script': 'Latin'}, 'mck': {'name': 'Mbunda', 'script': 'Latin'}, 'mer': {'name': 'Kimiiru', 'script': 'Latin'}, 'mgh': {'name': 'Makhuwa-Meetto', 'script': 'Latin'}, 'mgq': {'name': 'Malila', 'script': 'Latin'}, 'mgr': {'name': 'Mambwe-Lungu', 'script': 'Latin'}, 'mgw': {'name': 'Matumbi', 'script': 'Latin'}, 'mws': {'name': 'Mwimbi-Muthambi', 'script': 'Latin'}, 'myx': {'name': 'Masaaba', 'script': 'Latin'}, 'nba': {'name': 'Nyemba', 'script': 'Latin'}, 'nbl': {'name': 'IsiNdebele', 'script': 'Latin'}, 'ndc': {'name': 'Ndau', 'script': 'Latin'}, 'nde': {'name': 'IsiNdebele', 'script': 'Latin'}, 'ndh': {'name': 'Ndali', 'script': 'Latin'}, 'ndj': {'name': 'Ndamba', 'script': 'Latin'}, 'ndo': {'name': 'Ndonga', 'script': 'Latin'}, 'ngl': {'name': 'Lomwe', 'script': 'Latin'}, 'ngo': {'name': 'Ngoni', 'script': 'Latin'}, 'ngp': {'name': 'Ngulu', 'script': 'Latin'}, 'nih': {'name': 'Nyiha', 'script': 'Latin'}, 'nim': {'name': 'Nilamba / kinilyamba', 'script': 'Latin'}, 'nka': {'name': 'Nkoya / ShiNkoya', 'script': 'Latin'}, 'nnq': {'name': 'Ngindo', 'script': 'Latin'}, 'nse': {'name': 'Chinsenga', 'script': 'Latin'}, 'nso': {'name': 'Sepedi', 'script': 'Latin'}, 'nuj': {'name': 'Nyole', 'script': 'Latin'}, 'nya': {'name': 'Chichewa', 'script': 'Latin'}, 'nyd': {'name': 'Olunyole / Nyore', 'script': 'Latin'}, 'nyf': {'name': 'Giryama', 'script': 'Latin'}, 'nyk': {'name': 'Nyaneka', 'script': 'Latin'}, 'nym': {'name': 'Nyamwezi', 'script': 'Latin'}, 'nyn': {'name': 'Nyankore / Nyankole', 'script': 'Latin'}, 'nyo': {'name': 'Nyoro', 'script': 'Latin'}, 'nyu': {'name': 'Nyungwe', 'script': 'Latin'}, 'nyy': {'name': 'Nyakyusa-Ngonde / Kyangonde', 'script': 'Latin'}, 'poy': {'name': 'Pogolo / Shipogoro-Pogolo', 'script': 'Latin'}, 'rag': {'name': 'Lulogooli', 'script': 'Latin'}, 'rim': {'name': 'Nyaturu', 'script': 'Latin'}, 'rnd': {'name': 'Uruund', 'script': 'Latin'}, 'rng': {'name': 'Ronga / ShiRonga', 'script': 'Latin'}, 'rub': {'name': 'Gungu', 'script': 'Latin'}, 'run': {'name': 'Rundi / Kirundi', 'script': 'Latin'}, 'rwk': {'name': 'Rwa', 'script': 'Latin'}, 'sbp': {'name': 'Sangu', 'script': 'Latin'}, 'sbs': {'name': 'Kuhane', 'script': 'Latin'}, 'sby': {'name': 'Soli', 'script': 'Latin'}, 'sna': {'name': 'Shona', 'script': 'Latin'}, 'sng': {'name': 'Sanga / Kiluba', 'script': 'Latin'}, 'sop': {'name': 'Kisonge', 'script': 'Latin'}, 'sot': {'name': 'Sesotho', 'script': 'Latin'}, 'ssw': {'name': 'Siswati', 'script': 'Latin'}, 'suk': {'name': 'Sukuma', 'script': 'Latin'}, 'swa': {'name': 'Swahili', 'script': 'Latin'}, 'swc': {'name': 'Swahili Congo', 'script': 'Latin'}, 'swh': {'name': 'Swahili', 'script': 'Latin'}, 'swk': {'name': 'Sena, Malawi', 'script': 'Latin'}, 'sxb': {'name': 'Suba', 'script': 'Latin'}, 'thk': {'name': 'Tharaka', 'script': 'Latin'}, 'tke': {'name': 'Takwane', 'script': 'Latin'}, 'tlj': {'name': 'Talinga-Bwisi', 'script': 'Latin'}, 'tog': {'name': 'Tonga', 'script': 'Latin'}, 'toh': {'name': 'Gitonga', 'script': 'Latin'}, 'toi': {'name': 'Chitonga', 'script': 'Latin'}, 'tsc': {'name': 'Tshwa', 'script': 'Latin'}, 'tsn': {'name': 'Setswana', 'script': 'Latin'}, 'tso': {'name': 'Tsonga', 'script': 'Latin'}, 'ttj': {'name': 'Toro / Rutoro', 'script': 'Latin'}, 'tum': {'name': 'Chitumbuka', 'script': 'Latin'}, 'umb': {'name': 'Umbundu', 'script': 'Latin'}, 'ven': {'name': 'Tshivenda', 'script': 'Latin'}, 'vid': {'name': 'Chividunda', 'script': 'Latin'}, 'vif': {'name': 'Vili', 'script': 'Latin'}, 'vmk': {'name': 'Makhuwa-Shirima', 'script': 'Latin'}, 'vmw': {'name': 'Macua', 'script': 'Latin'}, 'vun': {'name': 'Kivunjo', 'script': 'Latin'}, 'wmw': {'name': 'Mwani', 'script': 'Latin'}, 'xho': {'name': 'Isixhosa', 'script': 'Latin'}, 'xog': {'name': 'Soga', 'script': 'Latin'}, 'yao': {'name': 'Yao / Chiyao', 'script': 'Latin'}, 'yom': {'name': 'Ibinda', 'script': 'Latin'}, 'zaj': {'name': 'Zaramo', 'script': 'Latin'}, 'zdj': {'name': 'Comorian, Ngazidja', 'script': 'Latin'}, 'zga': {'name': 'Kinga', 'script': 'Latin'}, 'ziw': {'name': 'Zigula', 'script': 'Latin'}, 'zul': {'name': 'Isizulu', 'script': 'Latin'}, 'mwn': {'name': 'Cinamwanga', 'script': 'Latin'}, 'loz': {'name': 'Silozi', 'script': 'Latin'}, 'lsm': {'name': 'Saamya-Gwe / Saamia', 'script': 'Latin'}, 'lto': {'name': 'Tsotso', 'script': 'Latin'}, 'lua': {'name': 'Tshiluba', 'script': 'Latin'}, 'lue': {'name': 'Luvale', 'script': 'Latin'}, 'lug': {'name': 'Luganda', 'script': 'Latin'}, 'lun': {'name': 'Lunda', 'script': 'Latin'}, 'lwg': {'name': 'Wanga', 'script': 'Latin'}, 'dwr': {'name': 'Dawro', 'script': 'Latin'}, 'gmv': {'name': 'Gamo', 'script': 'Latin'}, 'gof': {'name': 'Goofa', 'script': 'Latin'}, 'wal': {'name': 'Wolaytta', 'script': 'Latin'}, 'bci': {'name': 'Baoulé', 'script': 'Latin'}, 'cko': {'name': 'Anufo', 'script': 'Latin'}, 'fat': {'name': 'Fante', 'script': 'Latin'}, 'nzi': {'name': 'Nzema', 'script': 'Latin'}, 'sfw': {'name': 'Sehwi', 'script': 'Latin'}, 'twi': {'name': 'Twi', 'script': 'Latin'}, 'heh': {'name': 'Hehe', 'script': 'Latin'}, 'her': {'name': 'Herero', 'script': 'Latin'}, 'pem': {'name': 'Kipende', 'script': 'Latin'}, 'pkb': {'name': 'Kipfokomo / Pokomo', 'script': 'Latin'}, 'dib': {'name': 'Dinka, South Central', 'script': 'Latin'}, 'dik': {'name': 'Dinka, Southwestern', 'script': 'Latin'}, 'dip': {'name': 'Dinka, Northeastern', 'script': 'Latin'}, 'dks': {'name': 'Dinka, Southeastern', 'script': 'Latin'}, 'nus': {'name': 'Nuer', 'script': 'Latin'}, 'dow': {'name': 'Doyayo', 'script': 'Latin'}, 'kmy': {'name': 'Koma', 'script': 'Latin'}, 'gkn': {'name': 'Gokana', 'script': 'Latin'}, 'ogo': {'name': 'Khana', 'script': 'Latin'}, 'kqy': {'name': 'Koorete', 'script': 'Latin'}, 'fuh': {'name': 'Fulfulde, Western Niger', 'script': 'Latin'}, 'fuq': {'name': 'Fulfulde Central Eastern Niger', 'script': 'Latin'}, 'fuv': {'name': 'Fulfulde Nigeria', 'script': 'Arabic'}, 'fub': {'name': 'Fulfulde, Adamawa', 'script': 'Latin'}, 'gna': {'name': 'Kaansa', 'script': 'Latin'}, 'kbp': {'name': 'Kabiye', 'script': 'Latin'}, 'kdh': {'name': 'Tem', 'script': 'Latin'}, 'lee': {'name': 'Lyélé', 'script': 'Latin'}, 'mzw': {'name': 'Deg', 'script': 'Latin'}, 'nnw': {'name': 'Nuni, Southern', 'script': 'Latin'}, 'ntr': {'name': 'Delo', 'script': 'Latin'}, 'sig': {'name': 'Paasaal', 'script': 'Latin'}, 'sil': {'name': 'Sisaala, Tumulung', 'script': 'Latin'}, 'tpm': {'name': 'Tampulma', 'script': 'Latin'}, 'xsm': {'name': 'Kasem', 'script': 'Latin'}, 'vag': {'name': 'Vagla', 'script': 'Latin'}, 'acd': {'name': 'Gikyode', 'script': 'Latin'}, 'naw': {'name': 'Nawuri', 'script': 'Latin'}, 'ncu': {'name': 'Chunburung', 'script': 'Latin'}, 'nko': {'name': 'Nkonya', 'script': 'Latin'}, 'idu': {'name': 'Idoma', 'script': 'Latin'}, 'ige': {'name': 'Igede', 'script': 'Latin'}, 'yba': {'name': 'Yala', 'script': 'Latin'}, 'bqj': {'name': 'Bandial', 'script': 'Latin'}, 'csk': {'name': 'Jola Kasa', 'script': 'Latin'}, 'jib': {'name': 'Jibu', 'script': 'Latin'}, 'nnb': {'name': 'Nande / Ndandi', 'script': 'Latin'}, 'kln': {'name': 'Kalenjin', 'script': 'Latin'}, 'pko': {'name': 'Pökoot', 'script': 'Latin'}, 'krx': {'name': 'Karon', 'script': 'Latin'}, 'kia': {'name': 'Kim', 'script': 'Latin'}, 'cme': {'name': 'Cerma', 'script': 'Latin'}, 'akp': {'name': 'Siwu', 'script': 'Latin'}, 'lef': {'name': 'Lelemi', 'script': 'Latin'}, 'lip': {'name': 'Sekpele', 'script': 'Latin'}, 'snw': {'name': 'Selee', 'script': 'Latin'}, 'kdj': {'name': 'Ng’akarimojong', 'script': 'Latin'}, 'lot': {'name': 'Latuka', 'script': 'Latin'}, 'mas': {'name': 'Maasai', 'script': 'Latin'}, 'saq': {'name': 'Samburu', 'script': 'Latin'}, 'teo': {'name': 'Teso', 'script': 'Latin'}, 'tuv': {'name': 'Turkana', 'script': 'Latin'}, 'adh': {'name': 'Jopadhola / Adhola', 'script': 'Latin'}, 'alz': {'name': 'Alur', 'script': 'Latin'}, 'anu': {'name': 'Anyuak / Anuak', 'script': 'Latin'}, 'kdi': {'name': 'Kumam', 'script': 'Latin'}, 'laj': {'name': 'Lango', 'script': 'Latin'}, 'lth': {'name': 'Thur / Acholi-Labwor', 'script': 'Latin'}, 'luo': {'name': 'Dholuo / Luo', 'script': 'Latin'}, 'lwo': {'name': 'Luwo', 'script': 'Latin'}, 'mfz': {'name': 'Mabaan', 'script': 'Latin'}, 'shk': {'name': 'Shilluk', 'script': 'Latin'}, 'ach': {'name': 'Acholi', 'script': 'Latin'}, 'mpe': {'name': 'Majang', 'script': 'Latin'}, 'mcu': {'name': 'Mambila, Cameroon', 'script': 'Latin'}, 'bam': {'name': 'Bambara', 'script': 'Latin'}, 'dyu': {'name': 'Jula', 'script': 'Latin'}, 'knk': {'name': 'Kuranko', 'script': 'Latin'}, 'msc': {'name': 'Maninka, Sankaran', 'script': 'Latin'}, 'mfg': {'name': 'Mogofin', 'script': 'Latin'}, 'mnk': {'name': 'Mandinka', 'script': 'Latin'}, 'nza': {'name': 'Mbembe, Tigon', 'script': 'Latin'}, 'kbn': {'name': 'Kare', 'script': 'Latin'}, 'kzr': {'name': 'Karang', 'script': 'Latin'}, 'tui': {'name': 'Toupouri', 'script': 'Latin'}, 'xuo': {'name': 'Kuo', 'script': 'Latin'}, 'men': {'name': 'Mende', 'script': 'Latin'}, 'bex': {'name': 'Jur Modo', 'script': 'Latin'}, 'mgc': {'name': 'Morokodo', 'script': 'Latin'}, 'bcn': {'name': 'Bali', 'script': 'Latin'}, 'mzm': {'name': 'Mumuye', 'script': 'Latin'}, 'agq': {'name': 'Aghem', 'script': 'Latin'}, 'azo': {'name': 'Awing', 'script': 'Latin'}, 'bav': {'name': 'Vengo', 'script': 'Latin'}, 'bbj': {'name': "Ghomálá'", 'script': 'Latin'}, 'bbk': {'name': 'Babanki', 'script': 'Latin'}, 'bfd': {'name': 'Bafut', 'script': 'Latin'}, 'bmo': {'name': 'Bambalang', 'script': 'Latin'}, 'bmv': {'name': 'Bum', 'script': 'Latin'}, 'byv': {'name': 'Medumba', 'script': 'Latin'}, 'jgo': {'name': 'Ngomba', 'script': 'Latin'}, 'lmp': {'name': 'Limbum', 'script': 'Latin'}, 'mgo': {'name': "Meta'", 'script': 'Latin'}, 'mnf': {'name': 'Mundani', 'script': 'Latin'}, 'ngn': {'name': 'Bassa', 'script': 'Latin'}, 'nla': {'name': 'Ngombale', 'script': 'Latin'}, 'nnh': {'name': 'Ngiemboon', 'script': 'Latin'}, 'oku': {'name': 'Oku', 'script': 'Latin'}, 'yam': {'name': 'Yamba', 'script': 'Latin'}, 'ybb': {'name': 'Yemba', 'script': 'Latin'}, 'mdm': {'name': 'Mayogo', 'script': 'Latin'}, 'mbu': {'name': 'Mbula-Bwazza', 'script': 'Latin'}, 'gjn': {'name': 'Gonja', 'script': 'Latin'}, 'buy': {'name': 'Bullom So', 'script': 'Latin'}, 'gya': {'name': 'Gbaya, Northwest', 'script': 'Latin'}, 'bss': {'name': 'Akoose', 'script': 'Latin'}, 'bum': {'name': 'Bulu', 'script': 'Latin'}, 'dua': {'name': 'Douala', 'script': 'Latin'}, 'eto': {'name': 'Eton', 'script': 'Latin'}, 'ewo': {'name': 'Ewondo', 'script': 'Latin'}, 'iyx': {'name': 'yaka', 'script': 'Latin'}, 'khy': {'name': 'Kele / Lokele', 'script': 'Latin'}, 'kkj': {'name': 'Kako', 'script': 'Latin'}, 'koq': {'name': 'Kota', 'script': 'Latin'}, 'ksf': {'name': 'Bafia', 'script': 'Latin'}, 'lin': {'name': 'Lingala', 'script': 'Latin'}, 'mcp': {'name': 'Makaa', 'script': 'Latin'}, 'ngc': {'name': 'Ngombe', 'script': 'Latin'}, 'nxd': {'name': 'Ngando', 'script': 'Latin'}, 'ozm': {'name': 'Koonzime', 'script': 'Latin'}, 'tll': {'name': 'Otetela', 'script': 'Latin'}, 'tvu': {'name': 'Tunen', 'script': 'Latin'}, 'won': {'name': 'Wongo', 'script': 'Latin'}, 'yat': {'name': 'Yambeta', 'script': 'Latin'}, 'lem': {'name': 'Nomaande', 'script': 'Latin'}, 'loq': {'name': 'Lobala', 'script': 'Latin'}, 'ibb': {'name': 'Ibibio', 'script': 'Latin'}, 'efi': {'name': 'Efik', 'script': 'Latin'}, 'ann': {'name': 'Obolo', 'script': 'Latin'}, 'bfo': {'name': 'Birifor, Malba', 'script': 'Latin'}, 'bim': {'name': 'Bimoba', 'script': 'Latin'}, 'biv': {'name': 'Birifor, Southern', 'script': 'Latin'}, 'bud': {'name': 'Ntcham', 'script': 'Latin'}, 'bwu': {'name': 'Buli', 'script': 'Latin'}, 'dag': {'name': 'Dagbani', 'script': 'Latin'}, 'dga': {'name': 'Dagaare', 'script': 'Latin'}, 'dgd': {'name': 'Dagaari Dioula', 'script': 'Latin'}, 'dgi': {'name': 'Dagara, Northern', 'script': 'Latin'}, 'gng': {'name': 'Ngangam', 'script': 'Latin'}, 'gur': {'name': 'Farefare', 'script': 'Latin'}, 'gux': {'name': 'Gourmanchema', 'script': 'Latin'}, 'hag': {'name': 'Hanga', 'script': 'Latin'}, 'kma': {'name': 'Konni', 'script': 'Latin'}, 'kus': {'name': 'Kusaal', 'script': 'Latin'}, 'maw': {'name': 'Mampruli', 'script': 'Latin'}, 'mfq': {'name': 'Moba', 'script': 'Latin'}, 'mos': {'name': 'Moore', 'script': 'Latin'}, 'soy': {'name': 'Miyobe', 'script': 'Latin'}, 'xon': {'name': 'Konkomba', 'script': 'Latin'}, 'mwm': {'name': 'Sar', 'script': 'Latin'}, 'myb': {'name': 'Mbay', 'script': 'Latin'}, 'bjv': {'name': 'Bedjond', 'script': 'Latin'}, 'gqr': {'name': 'Gor', 'script': 'Latin'}, 'gvl': {'name': 'Gulay', 'script': 'Latin'}, 'ksp': {'name': 'Kabba', 'script': 'Latin'}, 'lap': {'name': 'Laka', 'script': 'Latin'}, 'sba': {'name': 'Ngambay', 'script': 'Latin'}, 'ndz': {'name': 'Ndogo', 'script': 'Latin'}, 'lnl': {'name': 'Banda, South Central', 'script': 'Latin'}, 'bun': {'name': 'Sherbro', 'script': 'Latin'}, 'gso': {'name': 'Gbaya, Southwest', 'script': 'Latin'}, 'mur': {'name': 'Murle', 'script': 'Latin'}, 'did': {'name': 'Didinga', 'script': 'Latin'}, 'tex': {'name': 'Tennet', 'script': 'Latin'}, 'vut': {'name': 'Vute', 'script': 'Latin'}, 'tcc': {'name': 'Datooga', 'script': 'Latin'}, 'kno': {'name': 'Kono', 'script': 'Latin'}, 'vai': {'name': 'Vai', 'script': 'Vai'}, 'tul': {'name': 'Kutule', 'script': 'Latin'}, 'bst': {'name': 'Basketo', 'script': 'Ethiopic'}, 'ffm': {'name': 'Fulfulde, Maasina', 'script': 'Latin'}, 'fue': {'name': 'Fulfulde, Borgu', 'script': 'Latin'}, 'fuf': {'name': 'Pular', 'script': 'Latin'}, 'zne': {'name': 'Zande / paZande', 'script': 'Latin'}, 'guw': {'name': 'Gun', 'script': 'Latin'}, 'amh': {'name': 'Amharic', 'script': 'Ethiopic'}, 'bsp': {'name': 'Baga Sitemu', 'script': 'Latin'}, 'bzw': {'name': 'Basa', 'script': 'Latin'}, 'nhu': {'name': 'Noone', 'script': 'Latin'}, 'avu': {'name': 'Avokaya', 'script': 'Latin'}, 'kbo': {'name': 'Keliko', 'script': 'Latin'}, 'lgg': {'name': 'Lugbara', 'script': 'Latin'}, 'log': {'name': 'Logo', 'script': 'Latin'}, 'luc': {'name': 'Aringa', 'script': 'Latin'}, 'xnz': {'name': 'Mattokki', 'script': 'Latin'}, 'uth': {'name': 'u̱t-Hun', 'script': 'Latin'}, 'kyf': {'name': 'Kouya', 'script': 'Latin'}, 'ijn': {'name': 'Kalabari', 'script': 'Latin'}, 'okr': {'name': 'Kirike', 'script': 'Latin'}, 'shj': {'name': 'Shatt', 'script': 'Latin'}, 'lro': {'name': 'Laro', 'script': 'Latin'}, 'mkl': {'name': 'Mokole', 'script': 'Latin'}, 'yor': {'name': 'Yoruba', 'script': 'Latin'}, 'bin': {'name': 'Edo', 'script': 'Latin'}, 'ish': {'name': 'Esan', 'script': 'Latin'}, 'etu': {'name': 'Ejagham', 'script': 'Latin'}, 'fon': {'name': 'Fon', 'script': 'Latin'}, 'ful': {'name': 'Fulah', 'script': 'Latin'}, 'gbr': {'name': 'Gbagyi', 'script': 'Latin'}, 'atg': {'name': 'Ivbie North-Okpela-Arhe', 'script': 'Latin'}, 'krw': {'name': 'Krahn, Western', 'script': 'Latin'}, 'wec': {'name': 'Guéré', 'script': 'Latin'}, 'har': {'name': 'Harari', 'script': 'Latin'}, 'igl': {'name': 'Igala', 'script': 'Latin'}, 'ktj': {'name': 'Krumen, Plapo', 'script': 'Latin'}, 'ted': {'name': 'Krumen, Tepo', 'script': 'Latin'}, 'asg': {'name': 'Cishingini', 'script': 'Latin'}, 'kdl': {'name': 'Tsikimba', 'script': 'Latin'}, 'tsw': {'name': 'Tsishingini', 'script': 'Latin'}, 'xrb': {'name': 'Karaboro, Eastern', 'script': 'Latin'}, 'kqs': {'name': 'Kisi', 'script': 'Latin'}, 'gbo': {'name': 'Grebo, Northern', 'script': 'Latin'}, 'lom': {'name': 'Loma', 'script': 'Latin'}, 'anv': {'name': 'Denya', 'script': 'Latin'}, 'ken': {'name': 'Kenyang', 'script': 'Latin'}, 'mfi': {'name': 'Wandala', 'script': 'Latin'}, 'mev': {'name': 'Maan / Mann', 'script': 'Latin'}, 'ngb': {'name': 'Ngbandi, Northern', 'script': 'Latin'}, 'fia': {'name': 'Nobiin', 'script': 'Latin'}, 'nwb': {'name': 'Nyabwa', 'script': 'Latin'}, 'mdy': {'name': 'Maale', 'script': 'Ethiopic'}, 'ebr': {'name': 'Ebrié', 'script': 'Latin'}, 'sef': {'name': 'Sénoufo, Cebaara', 'script': 'Latin'}, 'iri': {'name': 'Rigwe', 'script': 'Latin'}, 'izr': {'name': 'Izere', 'script': 'Latin'}, 'kcg': {'name': 'Tyap', 'script': 'Latin'}, 'spp': {'name': 'Sénoufo, Supyire', 'script': 'Latin'}, 'myk': {'name': 'Sénoufo, Mamara', 'script': 'Latin'}, 'dyi': {'name': 'Sénoufo, Djimini', 'script': 'Latin'}, 'sev': {'name': 'Sénoufo, Nyarafolo', 'script': 'Latin'}, 'tgw': {'name': 'Sénoufo, Tagwana', 'script': 'Latin'}, 'tem': {'name': 'Timne', 'script': 'Latin'}, 'tiv': {'name': 'Tiv', 'script': 'Latin'}, 'sgw': {'name': 'Sebat Bet Gurage', 'script': 'Latin'}, 'dnj': {'name': 'Dan', 'script': 'Latin'}, 'wol': {'name': 'Wolof', 'script': 'Latin'}, 'fak': {'name': 'Fang', 'script': 'Latin'}, 'sor': {'name': 'Somrai', 'script': 'Latin'}, 'bwr': {'name': 'Bura Pabir', 'script': 'Latin'}, 'kqp': {'name': 'Kimré', 'script': 'Latin'}, 'daa': {'name': 'Dangaléat', 'script': 'Latin'}, 'mmy': {'name': 'Migaama', 'script': 'Latin'}, 'hbb': {'name': 'Nya huba', 'script': 'Latin'}, 'aba': {'name': 'Abé / Abbey', 'script': 'Latin'}, 'adj': {'name': 'Adjukru  / Adioukrou', 'script': 'Latin'}, 'ati': {'name': 'Attié', 'script': 'Latin'}, 'avn': {'name': 'Avatime', 'script': 'Latin'}, 'nyb': {'name': 'Nyangbo', 'script': 'Latin'}, 'tcd': {'name': 'Tafi', 'script': 'Latin'}, 'bba': {'name': 'Baatonum', 'script': 'Latin'}, 'bky': {'name': 'Bokyi', 'script': 'Latin'}, 'bom': {'name': 'Berom', 'script': 'Latin'}, 'etx': {'name': 'Iten / Eten', 'script': 'Latin'}, 'gud': {'name': 'Dida, Yocoboué', 'script': 'Latin'}, 'igb': {'name': 'Ebira', 'script': 'Latin'}, 'ada': {'name': 'Dangme', 'script': 'Latin'}, 'gaa': {'name': 'Ga', 'script': 'Latin'}, 'ewe': {'name': 'Éwé', 'script': 'Latin'}, 'gol': {'name': 'Gola', 'script': 'Latin'}, 'yre': {'name': 'Yaouré', 'script': 'Latin'}, 'ibo': {'name': 'Igbo', 'script': 'Latin'}, 'ikk': {'name': 'Ika', 'script': 'Latin'}, 'ikw': {'name': 'Ikwere', 'script': 'Latin'}, 'iqw': {'name': 'Ikwo', 'script': 'Latin'}, 'izz': {'name': 'Izii', 'script': 'Latin'}, 'klu': {'name': 'Klao', 'script': 'Latin'}, 'gkp': {'name': 'Kpelle, Guinea', 'script': 'Latin'}, 'xpe': {'name': 'Kpelle', 'script': 'Latin'}, 'bov': {'name': 'Tuwuli', 'script': 'Latin'}, 'ajg': {'name': 'Aja', 'script': 'Latin'}, 'krs': {'name': 'Gbaya', 'script': 'Latin'}, 'xed': {'name': 'Hdi', 'script': 'Latin'}, 'niy': {'name': 'Ngiti', 'script': 'Latin'}, 'afr': {'name': 'Afrikaans', 'script': 'Latin'}, 'knf': {'name': 'Mankanya', 'script': 'Latin'}, 'moy': {'name': 'Shekkacho', 'script': 'Latin'}, 'iso': {'name': 'Isoko', 'script': 'Latin'}, 'oke': {'name': 'Okpe', 'script': 'Latin'}, 'urh': {'name': 'Urhobo', 'script': 'Latin'}, 'sus': {'name': 'Sosoxui', 'script': 'Latin'}, 'yal': {'name': 'Yalunka', 'script': 'Latin'}, 'bsc': {'name': 'Oniyan', 'script': 'Latin'}, 'cou': {'name': 'Wamey', 'script': 'Latin'}, 'wib': {'name': 'Toussian, Southern', 'script': 'Latin'}, 'moa': {'name': 'Mwan', 'script': 'Latin'}, 'ttr': {'name': 'Nyimatli', 'script': 'Latin'}, 'kub': {'name': 'Kutep', 'script': 'Latin'}, 'hau': {'name': 'Hausa', 'script': 'Latin'}, 'bcw': {'name': 'Bana', 'script': 'Latin'}, 'kvj': {'name': 'Psikye', 'script': 'Latin'}, 'giz': {'name': 'South Giziga', 'script': 'Latin'}, 'gnd': {'name': 'Zulgo-gemzek', 'script': 'Latin'}, 'maf': {'name': 'Mafa', 'script': 'Latin'}, 'meq': {'name': 'Merey', 'script': 'Latin'}, 'mfh': {'name': 'Matal', 'script': 'Latin'}, 'mfk': {'name': 'Mofu, North', 'script': 'Latin'}, 'mif': {'name': 'Mofu-Gudur', 'script': 'Latin'}, 'mlr': {'name': 'Vame', 'script': 'Latin'}, 'mqb': {'name': 'Mbuko', 'script': 'Latin'}, 'muy': {'name': 'Muyang', 'script': 'Latin'}, 'hna': {'name': 'Mina', 'script': 'Latin'}, 'bcy': {'name': 'Bacama', 'script': 'Latin'}, 'gde': {'name': 'Gude', 'script': 'Latin'}, 'moz': {'name': 'Mukulu', 'script': 'Latin'}, 'bib': {'name': 'Bisa', 'script': 'Latin'}, 'bqc': {'name': 'Boko', 'script': 'Latin'}, 'bus': {'name': 'Bokobaru', 'script': 'Latin'}, 'ndv': {'name': 'Ndut', 'script': 'Latin'}, 'snf': {'name': 'Noon', 'script': 'Latin'}, 'byf': {'name': 'Bété', 'script': 'Latin'}, 'lia': {'name': 'Limba, West-Central', 'script': 'Latin'}, 'mlg': {'name': 'Malagasy', 'script': 'Latin'}, 'tir': {'name': 'Tigrinya', 'script': 'Ethiopic'}, 'rif': {'name': 'Tarifit', 'script': 'Arabic'}, 'sbd': {'name': 'Samo, Southern', 'script': 'Latin'}, 'nhr': {'name': 'Naro', 'script': 'Latin'}, 'lmd': {'name': 'Lumun', 'script': 'Latin'}, 'shi': {'name': 'Tachelhit', 'script': 'Latin'}, 'gid': {'name': 'Gidar', 'script': 'Latin'}, 'xan': {'name': 'Xamtanga', 'script': 'Ethiopic'}, 'hgm': {'name': 'Hai|ǁom', 'script': 'Latin'}, 'sid': {'name': 'Sidama', 'script': 'Latin'}, 'kab': {'name': 'Kabyle', 'script': 'Latin'}, 'xtc': {'name': 'Katcha-Kadugli-Miri', 'script': 'Latin'}, 'kby': {'name': 'Kanuri, Manga', 'script': 'Latin'}, 'kri': {'name': 'Krio', 'script': 'Latin'}, 'wes': {'name': 'Pidgin, Cameroon', 'script': 'Latin'}, 'pcm': {'name': 'Nigerian Pidgin', 'script': 'Latin'}, 'naq': {'name': 'Khoekhoe', 'script': 'Latin'}, 'thv': {'name': 'Tamahaq, Tahaggart', 'script': 'Latin'}, 'gax': {'name': 'Oromo, Borana-Arsi-Guji', 'script': 'Ethiopic / Latin'}, 'gaz': {'name': 'Oromo, West Central', 'script': 'Ethiopic / Latin'}, 'orm': {'name': 'Oromo', 'script': 'Ethiopic / Latin'}, 'rel': {'name': 'Rendille', 'script': 'Latin'}, 'aar': {'name': 'Afar / Qafar', 'script': 'Latin'}, 'som': {'name': 'Somali', 'script': 'Latin'}, 'taq': {'name': 'Tamasheq', 'script': 'Latin'}, 'ttq': {'name': 'Tawallammat', 'script': 'Latin'}, 'dsh': {'name': 'Daasanach', 'script': 'Latin'}, 'mcn': {'name': 'Masana / Massana', 'script': 'Latin'}, 'mpg': {'name': 'Marba', 'script': 'Latin'}, 'bds': {'name': 'Burunge', 'script': 'Latin'}, 'ses': {'name': 'Songhay, Koyraboro Senni', 'script': 'Latin'}, 'cop': {'name': 'Coptic', 'script': 'Coptic'}, 'ber': {'name': 'Berber', 'script': 'Latin'}, 'crs': {'name': 'Seychelles Creole', 'script': 'Latin'}, 'mfe': {'name': 'Morisyen / Mauritian Creole', 'script': 'Latin'}, 'ktu': {'name': 'Kikongo', 'script': 'Latin'}, 'sag': {'name': 'Sango', 'script': 'Latin'}, 'kea': {'name': 'Kabuverdianu', 'script': 'Latin'}, 'pov': {'name': 'Guinea-Bissau Creole', 'script': 'Latin'}}
    return langs

  def classify(self, text, max_outputs=3):
    max_outputs = int(max_outputs)
    self.logger.info("Input text: {}".format(text))
    tokens = " ".join(self.tokenizer.EncodeAsPieces(text.strip()))
    # print(tokens)
    tokens = self.afrolid_task.source_dictionary.encode_line(tokens, add_if_not_exist=False,)
    # print("*****", tokens)
    # print (">>>>>>", torch.IntTensor(self.tokenizer.EncodeAsIds(text.strip())))
    # tokens=torch.IntTensor(self.tokenizer.EncodeAsIds(text))
    tokens=torch.IntTensor(tokens)
    # print(tokens)
    dummy_target = torch.tensor([-1])
    batch = data.language_pair_dataset.collate(
                samples=[{'id': -1, 'source': tokens, 'target':dummy_target}],  # bsz = 1
                pad_idx=self.afrolid_task.source_dictionary.pad(),
                eos_idx=self.afrolid_task.source_dictionary.eos(),
                left_pad_source=False,
                left_pad_target=False,
                input_feeding=True,
                pad_to_length={'source': 128, 'target': 1},
            )
    # print(batch)
    outputs = self.model(**batch['net_input'])
    probabilities, predictions_idx = F.softmax(outputs[0], dim=-1).topk(k=max_outputs)
    # print()
    results={}
    if max_outputs==1:
      label_name = self.afrolid_task.target_dictionary.string([predictions_idx])
      predicted_score = round(float(torch.squeeze(probabilities).detach().numpy())*100, 2)
      results[label_name]={'score':predicted_score, 'name': self.lang_info[label_name]['name'], 'script':self.lang_info[label_name]['script']}
    else:
      for score, prediction_idx in zip(torch.squeeze(probabilities),torch.squeeze(predictions_idx)):
        label_name = self.afrolid_task.target_dictionary.string([prediction_idx])
        predicted_score = round(float(torch.squeeze(score).detach().numpy())*100, 2)
        if predicted_score<=0:
          break
        # print(score, prediction_idx, label_name, predicted_score)
        # print(score, prediction_idx, label_name, predicted_score)
        results[label_name]={'score':predicted_score, 'name': self.lang_info[label_name]['name'], 'script':self.lang_info[label_name]['script']}
        
        # print ("ISO: {}\tName: {}\tScript: {}\tScore: {}%".format(
        #               label_name,
        #               self.lang_info[label_name]['name'], 
        #               self.lang_info[label_name]['script'],
        #               label_name))
      # print(text)
    return results
