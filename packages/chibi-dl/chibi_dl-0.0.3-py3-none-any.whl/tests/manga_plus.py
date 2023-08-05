import time
from unittest import TestCase, skip
from chibi_dl.site.crunchyroll import Crunchyroll
from chibi.file import Chibi_path
from chibi_dl.site.crunchyroll.exceptions import Episode_not_have_media
from vcr_unittest import VCRTestCase
from chibi.file.temp import Chibi_temp_path
from chibi_dl.site.manga_plus.site import Manga_plus
from unittest import TestCase

class Test_manga_plus:
    def _get_vcr_kwargs( self, **kw ):
        result = super()._get_vcr_kwargs( **kw )
        result[ 'ignore_localhost' ] = True
        return result

    def test_the_series_should_find_his_own_name( self ):
        self.assertIsInstance( self.site.series[0].name, str )

    def test_have_a_list_of_episodes( self ):
        self.assertTrue( self.site.series[0].episodes )
        for episode in self.site.series[0].episodes:
            self.assertTrue( episode.title )
            self.assertTrue( episode.fansub )
            self.assertTrue( episode.url )
            self.assertTrue( float( episode.number ) )

    def test_the_episode_should_have_a_list_of_images( self ):
        episode = self.site.series[0].episodes[0]
        self.assertTrue( episode.images_urls )

    def test_should_download_the_images_in_a_folder( self ):
        folder = Chibi_temp_path()
        episode = self.site.series[0].episodes[0]
        episode.download( folder )
        self.assertTrue( next( folder.ls() ) )
        for f in folder.ls():
            properties = f.open().properties
            self.assertGreater( properties.size, 1024 )

    def test_should_can_compress_the_download_files( self ):
        folder = Chibi_temp_path()
        folder_compress = Chibi_temp_path()
        episode = self.site.series[0].episodes[0]
        episode.download( folder )
        result = episode.compress( folder_compress, folder )
        self.assertIsInstance( result, Chibi_path )
        self.assertTrue( result.exists )
        self.assertTrue( result.endswith( ".cbz" ) )
        self.assertIn( result, folder_compress )

    def test_should_donwload_all_the_serie( self ):
        folder = Chibi_temp_path()
        serie = self.site.series[0]
        serie.download( folder )
        download_files = list( next( folder.ls() ).ls() )
        self.assertEqual( len( serie.episodes ), download_files )


@skip( "incomplete" )
class Test_spy_family( Test_manga_plus, TestCase ):
    def setUp( self ):
        super().setUp()
        self.site = Manga_plus()
        self.site.append(
            'https://mangaplus.shueisha.co.jp/titles/200031' )
