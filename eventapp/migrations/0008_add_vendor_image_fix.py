from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0007_vendor_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vendors/'),
        ),
    ]