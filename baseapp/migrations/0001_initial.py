# Generated by Django 2.2.6 on 2019-11-06 14:49

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=16)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Заказ оплачен'), (1, 'Товар отправлен'), (2, 'Товар доставлен')], default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateTimeField(null=True)),
                ('sum_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fio', models.CharField(default='', max_length=130)),
                ('email', models.EmailField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=128)),
                ('phone_number', models.CharField(default='', max_length=16)),
                ('info', models.TextField(default='', max_length=512)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='', max_length=3000)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.FloatField(default=0.0)),
                ('amount', models.IntegerField(default=0)),
                ('sell_state', models.IntegerField(choices=[(0, 'Есть в наличии'), (1, 'Нет в наличии'), (2, 'На заказ')], default=0)),
                ('photo', models.ImageField(default=None, upload_to='')),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sold', models.IntegerField(default=0)),
                ('category', models.ForeignKey(db_column='category', null=True, on_delete=django.db.models.deletion.SET_NULL, to='baseapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='SingleOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('sum_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseapp.Basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(default='', max_length=64)),
                ('value', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('products', models.ManyToManyField(to='baseapp.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='singleorder',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=1), name='amount1'),
        ),
        migrations.AddConstraint(
            model_name='singleorder',
            constraint=models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price1'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(price__gte=0), name='price0'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(discount__gte=0), name='discount0'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(discount__lte=100), name='discount1'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='amount0'),
        ),
        migrations.AddConstraint(
            model_name='basket',
            constraint=models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price2'),
        ),
    ]
