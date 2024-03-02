from django.db import models


class Category(models.Model):
    id              = models.BigAutoField(primary_key=True)
    name            = models.CharField(max_length=50, null=True)
    description     = models.TextField(null=True)

    class Meta:
        ordering    = ['id']

    def __str__(self):
        txt = '{\n'
        txt += 'ID \t: ' + str(self.id) + ',\n'
        txt += 'NAME \t: ' + str(self.name) + ',\n'
        txt += 'DESCRIPTION \t: ' + str(self.description) + ',\n'
        txt += '}\n'
        return txt