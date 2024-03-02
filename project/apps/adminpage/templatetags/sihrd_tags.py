from django import template

register = template.Library()


# ==============================================================================================
#                                          TAGS 
# ==============================================================================================

@register.filter('jenisfungsional')
def jenisfungsional(uid):
    data = {
      1 : 'Dosen',
      2 : 'Administrasi Umum dan Akademik',
      3 : 'Laboran',
      4 : 'Pustakawan',
      5 : 'Programer',
      6 : 'Teknisi',
      7 : 'Administrasi Keuangan',
    }
    try:
      return data[uid]
    except:
      return None



