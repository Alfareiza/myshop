import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from orders.models import OrderItem, Order


def export_to_csv(modeladmin, request, queryset):
    # modeladmin is an instanced object (ex.: <orders.admin.OrderAdmin object at 0x7fdba82e5210>)
    # modeladmin.model is the class of object (ex.: <class 'orders.models.Order'>)
    # opts or modeladmin.model._meta is <Options for Order> which his type is <class 'django.db.models.options.Options'>
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    # This means that the response must be handled as a csv
    response = HttpResponse(content_type='text/csv')

    # This means that the response has an attachment
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    """
    Make a list with all the fields of the model which hasn't many to many relation
    So, opts.get_fields() is for example:
        (<ManyToOneRel: orders.orderitem>, <django.db.models.fields.BigAutoField: id>,
         <django.db.models.fields.CharField: first_name>, <django.db.models.fields.CharField: last_name>,
        <django.db.models.fields.EmailField: email>, <django.db.models.fields.CharField: address>,
        <django.db.models.fields.CharField: postal_code>, <django.db.models.fields.CharField: city>,
        <django.db.models.fields.DateTimeField: created>, 
        <django.db.models.fields.DateTimeField: updated>,
        <django.db.models.fields.BooleanField: paid>)
    - His len is 11 because in this example the Order model has his 9 attrs + the id and the 
      many to many relation that is with OrderItem.
    - Every models.fields has at least, for example, the next attrs (applying an .__dict__):
        {'field': <django.db.models.fields.related.ForeignKey: order>, 
        'model': <class 'orders.models.Order'>, 
        'related_name': 'items', 'related_query_name': None, 
        'limit_choices_to': {}, 'parent_link': False, 
        'on_delete': <function CASCADE at 0x7fdbb8406b00>, 'symmetrical': False, 
        'multiple': True, 'field_name': 'id', 
        'related_model': <class 'orders.models.OrderItem'>, 
        'hidden': False, 'name': 'items', 'many_to_many': False, 'one_to_many': True}
    
    """
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # So, fields is a list of models.fields of the model received

    # Write a first line with the header of the csv
    writer.writerow([field.verbose_name for field in fields])

    # Write the rows with the info
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)  # Ex.: Get the first_name/last_name/... of the model
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    # An TabularInline allow to include a model in the same
    # page of modification of a model related to him
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
