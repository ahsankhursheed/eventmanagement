from django.db import migrations, models
import datetime
from django.utils.timezone import utc

class Migration(migrations.Migration):

    dependencies = [
        ('app_name', 'previous_migration_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelname',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now(utc) - datetime.timedelta(days=2)),
            preserve_default=False,
        ),
    ]