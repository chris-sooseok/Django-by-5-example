
# Chapter 12: building e-learning platform

# building course models
Each course will be divided into a configurable number of modules, and each module will contain a configurable number of contents.

# Using fixtures to provide initial data for models

dumpdata: dumps data from db into the standard output. The resulting data structure includes information about the model and its fields for django to be able to load it into db
loaddata: load data structure into db

# Creating models for polymorphic content
django offers three options to use model inheritance
- abstract models: Useful when you want to put some common information into several models
- Multi-table model inheritance: In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model
- Proxy models: Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options

# Creating custom model fields
you can also create your own model fields to store custom data or alter the behavior of existing
fields. Custom fields allow you to store unique data types, implement custom validations, encapsulate
complex data logic related to the field, or define specific rendering forms using custom widgets.

# Chapter 13: Creating a content management system

# class-based views
When you need to provide a specific behavior for several class-based views, it is recommended that you use mixins.
Mixins are a type of class designed to supply methods to other classes but aren’t intended to be used independently. This allows you to develop shared functionalities that can be incorporated into various classes in a modular manner, simply by having those classes inherit from mixins. 
The concept is similar to a base class, but you can use multiple mixins to extend the funtionality of a given class

# Working with groups and permissions
By default, Django generates four permissions for each model in the installed applications: add, view, change, and delete.

# using formsets for source modules
formsets manage multiple instances of a certain form

# reordering modules and their contents
HTML Drag and Drop API to use fetch api to send an async http request that stores the new module order

python -m pip install django-braces==1.15.0
django-braces contains a collection of generic mexins that provides additiona features for class-based views that are useful for various common scenarios

