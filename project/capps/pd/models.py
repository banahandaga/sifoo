from django.db import models

# Data pokok PTMA: definisi dari kantro PP
class Tptm(models.Model):
        no = models.IntegerField(
            help_text="nomer urut ptma",
            default=0)
        kode = models.CharField(
            help_text="kode perguruan tinggi dari forlap dikti",
            max_length=20, blank=True, default='')
        nama = models.TextField(null=True)
        jenis = models.CharField(
            help_text="Akademik, Sekolah Tinggi, Institute dan Universitas",
            max_length=20, blank=True, default='')
        status = models.IntegerField(
            help_text="0:Tutup; 1: aktif; 2: Alih Bentuk",
            default=1)
        org = models.IntegerField(
            help_text="1: Aisyiyah; 2: Muhammadiyah",
            default=2)
        nama_pp = models.TextField(null=True)
        updated = models.DateTimeField(auto_now=True)
        # Tpt = models.ForeignKey(Tpt, related_name="Tptm", on_delete=models.CASCADE,default=1)
        def __str__(self):
            return self.kode
            
        class Meta:
            verbose_name = 'PTMA'
            verbose_name_plural = 'PTMA'   
