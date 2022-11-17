from biomage_programmatic_interface import Biomage

c = Biomage.authenticate('kristian@biomage.net', 'ZgC7drZhymsPs8$E', 'local')

c.plot.upload_image('1de7757a6767aef0ab701d423c27ca61', '../custom_plot.jpg')
c.plot.upload_image('1de7757a6767aef0ab701d423c27ca61', '../custom_plot2.jpeg')

