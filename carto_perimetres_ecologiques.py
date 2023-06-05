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
        self.layout_carto_perim_eco = None


    def initialisation(self):

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


        if len(self.dlg.mComboBox_3.checkedItems()) > 4:
            self.QMBquestion = QMessageBox.question(iface.mainWindow(), u"Attention !",
                                                    "Le nombre de périmètres écologiques est limité à 4 par défaut pour des questions de performances. Souhaitez vous tout de même charger les " + str(
                                                        len(self.dlg.mComboBox_3.checkedItems())) + " périmètres sélectionnés ? (risque de plantage de QGIS)",
                                                    QMessageBox.Yes | QMessageBox.No)

            if self.QMBquestion == QMessageBox.No:
                print("Annulation du chargement des couches")
                execute_code = False  # Use a flag variable to determine whether to execute the code or not


        execute_code = len(self.dlg.mComboBox_3.checkedItems()) < 4 or self.QMBquestion == QMessageBox.Yes

        if execute_code: #the flag variable execute_code is set to True when the condition len(self.dlg.mComboBox_3.checkedItems()) < 4 or self.QMBquestion == QMessageBox.Yes is True. If either of these conditions is True, the flag will be True, and the code block will be executed.
            for item in self.test:
                item.update({"version": "1.0.0", "request": "GetFeature"})
                url = item['url']
                typename = item['nom_technique']
                request = item['request']
                version = item['version']
                final_url = f"{url}VERSION={version}&TYPENAME={typename}&request={request}"
                uri = final_url

                layer_name = item['Nom_couche_plugin']
                existing_layers = QgsProject.instance().mapLayersByName(layer_name)

                if not existing_layers:
                    self.perim_eco_layer = QgsVectorLayer(uri, layer_name, "WFS")
                    self.perim_eco_layer.loadNamedStyle(
                        os.path.dirname(__file__) + '/styles_couches/' + layer_name + '.qml')
                    self.perim_eco_layer.triggerRepaint()

                    QgsProject.instance().addMapLayer(self.perim_eco_layer)
                else:
                    print(f"La couche '{layer_name}' est déjà chargée dans QGIS")

    def mise_en_page(self):

        vlayer = QgsProject.instance().mapLayersByName("Sites gérés CEN-NA")[0]
        depts_NA = QgsProject.instance().mapLayersByName("Département")[0]


        myRenderer = depts_NA.renderer()

        if depts_NA.geometryType() == QgsWkbTypes.PolygonGeometry:
            mySymbol1 = QgsSymbol.defaultSymbol(depts_NA.geometryType())
            fill_layer = QgsSimpleFillSymbolLayer.create(
                {'color': '255,255,255,0', 'outline_color': '0,0,0,255', 'outline_width': '0.1'}
            )
            mySymbol1.changeSymbolLayer(0, fill_layer)
            myRenderer.setSymbol(mySymbol1)

        depts_NA.triggerRepaint()

        vlayer.removeSelection()

        for sites in self.dlg.mComboBox.checkedItems():

            vlayer.selectByExpression('"nom_site"= \'{0}\''.format(sites.replace("'", "''")), QgsVectorLayer.AddToSelection)

        iface.mapCanvas().zoomToSelected(vlayer)


        rules = (
            ('Site CEN sélectionné', "is_selected()", 'red'),
        )

        # create a new rule-based renderer
        symbol = QgsSymbol.defaultSymbol(vlayer.geometryType())
        renderer = QgsRuleBasedRenderer(symbol)

        # get the "root" rule
        root_rule = renderer.rootRule()

        for label, expression, color_name in rules:
            # create a clone (i.e. a copy) of the default rule
            rule = root_rule.children()[0].clone()
            # set the label, expression and color
            rule.setLabel(label)
            rule.setFilterExpression(expression)
            symbol_layer = rule.symbol().symbolLayer(0)
            color = symbol_layer.color()
            generator = QgsGeometryGeneratorSymbolLayer.create({})
            generator.setSymbolType(QgsSymbol.Marker)
            generator.setGeometryExpression("centroid($geometry)")
            generator.setColor(QColor('Red'))
            rule.symbol().setColor(QColor(color_name))
            # set the scale limits if they have been specified
            # append the rule to the list of rules
            rule.symbol().changeSymbolLayer(0, generator)
            root_rule.appendChild(rule)

        # delete the default rule
        root_rule.removeChildAt(0)

        # apply the renderer to the layer
        vlayer.setRenderer(renderer)
        # refresh the layer on the map canvas
        vlayer.triggerRepaint()

        if self.dlg.radioButton.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("Fond ortho IGN 2021")[0]
        elif self.dlg.radioButton_2.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("OSM")[0]
        elif self.dlg.radioButton_3.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("SCAN25 IGN")[0]
        elif self.dlg.radioButton_4.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("Plan IGN")[0]

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

        self.my_map1.setScale(self.my_map1.scale() * 4.5)

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

        legend.model().rootGroup().removeLayer(vlayer)
        legend.model().rootGroup().removeLayer(fond_carte)
        legend.model().rootGroup().removeLayer(depts_NA)

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
        title.attemptResize(QgsLayoutSize(297, 7, QgsUnitTypes.LayoutMillimeters))
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
        subtitle.attemptResize(QgsLayoutSize(297, 7, QgsUnitTypes.LayoutMillimeters))
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

