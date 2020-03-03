from django.test import TestCase
from .models import Editor,album,tags
import datetime as dt



class EditorTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')

    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.james,Editor))

     # Testing Save Method
    def test_save_method(self):
        self.james.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)
class AlbumTestClass(TestCase):

    def setUp(self):
        # Creating a new editor and saving it
        self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')
        self.james.save_editor()

        # Creating a new tag and saving it
        self.new_tag = tags(name = 'testing')
        self.new_tag.save()

        self.new_album= Album(title = 'Test Album',post = 'This is a random test Post',editor = self.james)
        self.album.save()

        self.new_album.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Album.objects.all().delete()

    def test_get_albumimage(self):
        albumimage = album.albumimage()
        self.assertTrue(len(albumimage)>0)

     def test_get_app_by_date(self):
        test_date = '2020-02-25'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        app_by_date =Album.albumimage(date)
        self.assertTrue(len(app_by_date) == 0)