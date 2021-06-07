# Generated by Django 3.0.8 on 2021-06-07 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='user_interests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sports', multiselectfield.db.fields.MultiSelectField(choices=[('Cricket', 'Cricket'), ('Kabadi', 'Kabadi'), ('BasketBall', 'Basketball'), ('Volleyball', 'Volleyball'), ('Hockey', 'Hockey')], max_length=300, null=True)),
                ('music', multiselectfield.db.fields.MultiSelectField(choices=[('Rock', 'Rock'), ('HipHop', 'HipHop'), ('PopMusic', 'PopMusic'), ('Instrumental', 'Instrumental'), ('Disco', 'Disco')], max_length=300, null=True)),
                ('science', multiselectfield.db.fields.MultiSelectField(choices=[('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('World', 'World'), ('Homescience', 'Homescience'), ('Purescience', 'Purescience')], max_length=300, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_complete', models.BooleanField(default=False)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=128)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.Option')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey_app.Submission')),
            ],
        ),
    ]