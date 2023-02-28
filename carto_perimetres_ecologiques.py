import urllib
import csv
import io

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import Qt
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtXml import QDomDocument
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .map_cen_dialog import MapCENDialog
import os.path


from datetime import date

class module_perim_eco():

    def __init__(self):
        self.dlg = None
        self.test = None
        self.layout_carto_perim_eco = None


    def initialisation2(self):

        #On lit le fichier csv contenant les flux CEN sous forme de dictionnaire et on en extrait tous les noms techniques correspondant à la catégorie "Périmètres écologiques":
        url_open = urllib.request.urlopen("https://raw.githubusercontent.com/CEN-Nouvelle-Aquitaine/fluxcen/main/flux.csv")

        #The error message "I/O operation on closed file" indicates that we're trying to read from a file-like object that has already been closed.
        #When using urllib.request.urlopen() to fetch the CSV data but the file-like object returned by urlopen() is being closed when the csvReader list is created. This means that when we try to use csvReader again, the file-like object is no longer open and we can't read from it.
        # To avoid this issue, you can fetch the CSV data and store it in a separate variable before using it to create the csvReader:

        flux = url_open.read().decode('utf-8')

        #problème lors d'une seconde utilisation du dictionnaire csvReader; solution: https://stackoverflow.com/questions/20507228/python-how-do-i-use-dictreader-twice
        csvReader = list(csv.DictReader(io.StringIO(flux), delimiter=';'))

        #on filtre la liste des dictionnaires afin de ne garder que les données correspondantes à la catégorie "Périmètres écologiques:
        filtered_rows = [row for row in csvReader if row['categorie'] == 'Périmètres écologiques']

        nom_perim_eco = []

        for item in filtered_rows:
            #On récupère tous les noms des flux pour les ajouter à une liste qui servira ensuite à populer la combobox_3
            nom_perim_eco.append(item['Nom_couche_plugin'])

        #On fait apparaitre la comboBox lorsque le choix "périmetre eco" est sélectionné (idem pour le label_15) :
        if not self.dlg.mComboBox_3.isVisible():
            self.dlg.mComboBox_3.show()

        self.dlg.mComboBox_3.addItems(nom_perim_eco)

        self.dlg.label_15.setText("Périmètres écologiques :")
        self.dlg.label_15.show()


    def chargement_perim_eco(self):

        # On lit le fichier csv contenant les flux CEN sous forme de dictionnaire et on en extrait tous les noms techniques correspondant à la catégorie "Périmètres écologiques":
        url_open = urllib.request.urlopen(
            "https://raw.githubusercontent.com/CEN-Nouvelle-Aquitaine/fluxcen/main/flux.csv")

        # The error message "I/O operation on closed file" indicates that we're trying to read from a file-like object that has already been closed.
        # When using urllib.request.urlopen() to fetch the CSV data but the file-like object returned by urlopen() is being closed when the csvReader list is created. This means that when we try to use csvReader again, the file-like object is no longer open and we can't read from it.
        # To avoid this issue, you can fetch the CSV data and store it in a separate variable before using it to create the csvReader:

        flux = url_open.read().decode('utf-8')

        # problème lors d'une seconde utilisation du dictionnaire csvReader; solution: https://stackoverflow.com/questions/20507228/python-how-do-i-use-dictreader-twice
        self.csvReader = list(csv.DictReader(io.StringIO(flux), delimiter=';'))

        #On charge les sites gérés :
        self.test = [row for row in self.csvReader if row['Nom_couche_plugin'] in self.dlg.mComboBox_3.checkedItems()]

        for item in self.test:
            item.update({"version": "1.0.0", "request": "GetFeature"})
            url = item['url']
            typename = item['nom_technique']
            request = item['request']
            version = item['version']
            final_url = f"{url}VERSION={version}&TYPENAME={typename}&request={request}"
            uri = final_url

            self.perim_eco_layer = QgsVectorLayer(uri, item['Nom_couche_plugin'], "WFS")
            self.perim_eco_layer.loadNamedStyle(os.path.dirname(__file__) + '/styles_couches/' + item['Nom_couche_plugin'] +'.qml')
            self.perim_eco_layer.triggerRepaint()

            QgsProject.instance().addMapLayer(self.perim_eco_layer)



    def mise_en_page(self):

        self.dlg.horizontalSlider.setValue(0)

        # ajout de la date, l'auteur, source etc...
        date_du_jour = date.today().strftime("%d/%m/%Y")

        # QgsProject.instance().layerTreeRoot().findLayer(self.vlayer.id()).setItemVisibilityChecked(False)

        ## Ajout de la mise en page au composeur de carte:
        project = QgsProject.instance()
        self.manager = project.layoutManager()
        layout_name = 'Mise en page automatique MapCEN (Périmètres écologiques)'
        layouts_list = self.manager.printLayouts()
        # Just 4 debug
        # remove any duplicate layouts
        for self.layout in layouts_list:
            if self.layout.name() == layout_name:
                self.manager.removeLayout(self.layout)

        self.layout = QgsPrintLayout(project)
        self.layout.initializeDefaults()
        self.layout.setName(layout_name)

        ## Add map to layout
        self.my_map1 = QgsLayoutItemMap(self.layout)

        # Charger une carte vide
        self.my_map1.setRect(20, 20, 20, 20)


        for item in [row for row in self.csvReader if row['Nom_couche_plugin'] in self.dlg.mComboBox_3.checkedItems()]:
            for layer in QgsProject.instance().mapLayersByName(item['Nom_couche_plugin'][0]):
                self.my_map1.setLayers(layer)


        # Mettre le canvas courant comme emprise
        self.my_map1.setExtent(iface.mapCanvas().extent())

        self.my_map1.setScale(self.my_map1.scale() * 3)

        # Position de la carte dans le composeur
        self.my_map1.attemptMove(QgsLayoutPoint(5, 29, QgsUnitTypes.LayoutMillimeters))

        #on dimensionne le rendu de la carte (pour référence la page totale est une page A4 donc 297*210)
        self.my_map1.attemptResize(QgsLayoutSize(287, 135, QgsUnitTypes.LayoutMillimeters))
        self.my_map1.refresh()

        self.my_map1.setBackgroundColor(QColor(255, 255, 255, 255))
        self.my_map1.setFrameEnabled(True)
        self.layout.addLayoutItem(self.my_map1)

        self.my_map1.setId("carte_principale_perim_eco")
        # print(self.my_map1.id())


        ## Ajout de la legende :
        legend = QgsLayoutItemLegend(self.layout)
        # legend.setTitle('Legende')
        legend.adjustBoxSize()
        legend.setFrameEnabled(False)
        legend.setAutoUpdateModel(False)

        root = legend.model().rootGroup()
        group_perim_eco = root.addGroup("Périmètres écologiques")

        for item in [row for row in self.csvReader if row['Nom_couche_plugin'] in self.dlg.mComboBox_3.checkedItems()]:
            for layer in QgsProject.instance().mapLayersByName(item['Nom_couche_plugin'][0]):
                group_perim_eco.addLayer(layer)

        legend.updateLegend()

        legend.setLegendFilterByMapEnabled(True)
        self.layout.addItem(legend)
        legend.setLinkedMap(self.my_map1)

        # layer_to_remove = self.fond
        # legend.model().rootGroup().removeLayer(layer_to_remove)

        legend.attemptMove(QgsLayoutPoint(7, 165, QgsUnitTypes.LayoutMillimeters))

        legend.setColumnCount(2)
        legend.setEqualColumnWidth(False)
        legend.setSplitLayer(True)
        legend.setColumnSpace(10)

        legend.setWrapString("*")

        legend.adjustBoxSize()

        self.layout.refresh()



        ## Ajout d'un titre à la mise en page
        title = QgsLayoutItemLabel(self.layout)
        self.layout.addLayoutItem(title)
        titre = str(', '.join(self.dlg.mComboBox.checkedItems()))
        title.setText(titre)
        title.setFont(QFont("Calibri", 16, QFont.Bold))
        title.attemptMove(QgsLayoutPoint(5, 6, QgsUnitTypes.LayoutMillimeters))
        title.attemptResize(QgsLayoutSize(287, 7, QgsUnitTypes.LayoutMillimeters))
        title.setHAlign(Qt.AlignHCenter)
        title.setVAlign(Qt.AlignHCenter)
        title.adjustSizeToText()
        self.layout.addItem(title)


        ## Ajout d'un sous-titre à la mise en page
        subtitle = QgsLayoutItemLabel(self.layout)
        self.layout.addLayoutItem(subtitle)
        titre = str("Périmètres d'intérêts écologiques à proximité des sites (" + date_du_jour +")")
        subtitle.setText(titre)
        subtitle.setFont(QFont("Calibri", 14))
        subtitle.attemptMove(QgsLayoutPoint(5, 14, QgsUnitTypes.LayoutMillimeters))
        subtitle.attemptResize(QgsLayoutSize(287, 7, QgsUnitTypes.LayoutMillimeters))
        subtitle.setHAlign(Qt.AlignHCenter)
        subtitle.setVAlign(Qt.AlignHCenter)
        subtitle.adjustSizeToText()
        self.layout.addItem(subtitle)


        ## Ajout du logo CEN NA en haut à gauche de la page
        layoutItemPicture = QgsLayoutItemPicture(self.layout)
        layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
        layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
        layoutItemPicture.setPicturePath(os.path.dirname(__file__) + '/logo.jpg')


        # dim_image_original = [250, 84]
        # new_dim = [i * 0.15 for i in dim_image_original]
        layoutItemPicture.attemptMove(QgsLayoutPoint(5.5, 3.5, QgsUnitTypes.LayoutMillimeters))
        layoutItemPicture.attemptResize(QgsLayoutSize(720, 249, QgsUnitTypes.LayoutPixels))

        self.layout.addLayoutItem(layoutItemPicture)


        ## Ajout de l'échelle à la mise en page
        self.scalebar = QgsLayoutItemScaleBar(self.layout)
        self.scalebar.setStyle('Single Box')
        self.scalebar.setLinkedMap(self.my_map1)
        self.scalebar.applyDefaultSize()
        self.scalebar.applyDefaultSettings()

        self.scalebar.setNumberOfSegments(2)
        self.scalebar.setNumberOfSegmentsLeft(0)

        self.layout.addLayoutItem(self.scalebar)
        self.scalebar.attemptMove(QgsLayoutPoint(206, 185, QgsUnitTypes.LayoutMillimeters))
        self.scalebar.setFixedSize(QgsLayoutSize(50, 15))


        # ajout de la fleche du Nord
        north = QgsLayoutItemPicture(self.layout)
        north.setPicturePath(os.path.dirname(__file__) + "/NorthArrow_02.svg")
        self.layout.addLayoutItem(north)
        north.attemptResize(QgsLayoutSize(19, 14, QgsUnitTypes.LayoutMillimeters))
        north.attemptMove(QgsLayoutPoint(273, 184, QgsUnitTypes.LayoutMillimeters))



        info = ["Réalisation : " + "DSI / CEN Nouvelle-Aquitaine (" + date_du_jour + ") \n Source: © Fond carto IGN, cadastre ETALAB, MNHN-INPN, CEN Nouvelle-Aquitaine"]
        credit_text = QgsLayoutItemLabel(self.layout)
        credit_text.setText(info[0])
        credit_text.setFont(QFont("Calibri", 11))
        self.layout.addLayoutItem(credit_text)
        credit_text.attemptMove(QgsLayoutPoint(158.413, 148, QgsUnitTypes.LayoutMillimeters))
        credit_text.attemptResize(QgsLayoutSize(133.737, 16, QgsUnitTypes.LayoutMillimeters))
        credit_text.setBackgroundEnabled(True)
        credit_text.setBackgroundColor(QColor('white'))
        credit_text.setItemOpacity(0.7)
        credit_text.setHAlign(Qt.AlignHCenter)
        credit_text.setVAlign(Qt.AlignVCenter)
        # credit_text.adjustSizeToText()


        # Finally add layout to the project via its manager
        self.manager.addLayout(self.layout)


        self.layout_carto_perim_eco = QgsProject.instance().layoutManager().layoutByName('Mise en page automatique MapCEN (Périmètres écologiques)').clone()

        self.dlg.graphicsView.setScene(self.layout_carto_perim_eco)


    def get_test(self):
        return self.test

