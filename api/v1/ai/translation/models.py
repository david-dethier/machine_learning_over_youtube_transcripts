from django.db import models


# Create your models here.
class TranslationModel(models.Model):
    LANGUAGES = [
        ("ar_AR", "Arabic"), ("cs_CZ", "Czech"), ("de_DE", "German"), ("en_XX", "English"), ("es_XX", "Spanish"),
        ("et_EE", "Estonian"), ("fi_FI", "Finnish"),
        ("fr_XX", "French"), ("gu_IN", "Gujarati"), ("hi_IN", "Hindi"), ("it_IT", "Italian"),
        ("ja_XX", "Japanese"), ("kk_KZ", "Kazakh"), ("ko_KR", "Korean"),
        ("lt_LT", "Lithuanian"), ("lv_LV", "Latvian"), ("my_MM", "Burmese"), ("ne_NP", "Nepali"),
        ("nl_XX", "Dutch"), ("ro_RO", "Romanian"), ("ru_RU", "Russian"),
        ("si_LK", "Sinhala"), ("tr_TR", "Turkish"), ("vi_VN", "Vietnamese"), ("zh_CN", "Chinese"),
        ("af_ZA", "Afrikaans"), ("az_AZ", "Azerbaijani"),
        ("bn_IN", "Bengali"), ("fa_IR", "Persian"), ("he_IL", "Hebrew"), ("hr_HR", "Croatian"),
        ("id_ID", "Indonesian"), ("ka_GE", "Georgian"),
        ("km_KH", "Khmer"), ("mk_MK", "Macedonian"), ("ml_IN", "Malayalam"), ("mn_MN", "Mongolian"),
        ("mr_IN", "Marathi"), ("pl_PL", "Polish"),
        ("ps_AF", "Pashto"), ("pt_XX", "Portuguese"), ("sv_SE", "Swedish"), ("sw_KE", "Swahili"),
        ("ta_IN", "Tamil"), ("te_IN", "Telugu"), ("th_TH", "Thai"),
        ("tl_XX", "Tagalog"), ("uk_UA", "Ukrainian"), ("ur_PK", "Urdu"), ("xh_ZA", "Xhosa"), ("gl_ES", "Galician"),
        ("sl_SI", "Slovene")
    ]
    
    from_lang = models.CharField(max_length=5, choices=LANGUAGES)
    to_lang = models.CharField(max_length=5, choices=LANGUAGES)
    input = models.TextField()
