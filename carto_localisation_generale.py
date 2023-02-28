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


class module_loc_generale():

    def __init__(self):
        self.dlg = None
        self.layout_carto_generale = None


    def mise_en_page(self):

        layer = QgsProject.instance().mapLayersByName("Parcelles CEN NA en MFU")[0]
        vlayer = QgsProject.instance().mapLayersByName("Sites gérés CEN-NA")[0]
        depts_NA = QgsProject.instance().mapLayersByName("Département")[0]

        if self.dlg.radioButton.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("Fond ortho IGN 2021")[0]
        elif self.dlg.radioButton_2.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("OSM")[0]
        elif self.dlg.radioButton_3.isChecked() == True:
            fond_carte = QgsProject.instance().mapLayersByName("SCAN25 IGN")[0]

        self.dlg.horizontalSlider.setValue(0)

        # ajout de la date, l'auteur, source etc...
        date_du_jour = date.today().strftime("%d/%m/%Y")

        # QgsProject.instance().layerTreeRoot().findLayer(self.vlayer.id()).setItemVisibilityChecked(False)

        ## Ajout de la mise en page au composeur de carte:

        project = QgsProject.instance()
        self.manager = project.layoutManager()
        layout_name = 'Mise en page automatique MapCEN (Carto de localisation générale)'
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


        self.my_map1.setLayers([layer, fond_carte])


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

        self.my_map1.setId("carte_principale_loc_generale")
        # print(self.my_map1.id())

        # --- create map item 2 (shapefile, raster 2, basemap)

        my_map2 = QgsLayoutItemMap(self.layout)
        my_map2.setRect(20, 20, 20, 20)
        my_map2.setPos(228, 27)
        my_map2.setFrameEnabled(False)

        my_map2.setLayers([vlayer, depts_NA])

        ## Ajustement de l'emprise de la couche depts_CEN-NA au CRS 2154 :

        crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")

        # recherche du CRS du projet pour réaliser transformation (normalement 2154):
        crsDest = QgsCoordinateReferenceSystem(QgsCoordinateReferenceSystem("EPSG:2154"))
        transformContext = QgsProject.instance().transformContext()
        xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)

        # forward transformation: src -> dest
        extent = xform.transform(depts_NA.extent())


        my_map2.setExtent(extent)
        my_map2.setScale(30000000)

        my_map2.attemptResize(QgsLayoutSize(65, 65, QgsUnitTypes.LayoutMillimeters))

        self.layout.addLayoutItem(my_map2)


        ## Ajout de la legende :
        legend = QgsLayoutItemLegend(self.layout)
        # legend.setTitle('Legende')
        legend.adjustBoxSize()
        legend.setFrameEnabled(False)
        legend.setAutoUpdateModel(False)

        root = QgsLayerTree()
        # root.addLayer(layer).setUseLayerName(False)
        # root.addLayer(layer).setName("Types de maîtrise")

        legend.updateLegend()

        legend.setLegendFilterByMapEnabled(True)
        self.layout.addItem(legend)
        legend.setLinkedMap(self.my_map1)

        legend.model().rootGroup().removeLayer(fond_carte)
        legend.model().rootGroup().removeLayer(vlayer)

        legend.attemptMove(QgsLayoutPoint(7, 165, QgsUnitTypes.LayoutMillimeters))

        # legend.setColumnCount(3)

        legend.setColumnCount(2)
        legend.setEqualColumnWidth(False)
        legend.setSplitLayer(True)
        legend.setColumnSpace(10)

        legend.setWrapString("*")


        legend.setWrapString("*")

        legend.adjustBoxSize()

        self.layout.refresh()



        ## Ajout d'un titre à la mise en page
        title = QgsLayoutItemLabel(self.layout)
        self.layout.addLayoutItem(title)
        titre = str(', '.join(self.dlg.mComboBox.checkedItems()) + " (" + vlayer.selectedFeatures()[0]["codesite"][:2] + ")")
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
        titre = str("Localisation générale (" + date_du_jour +")")
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

        self.layout_carto_generale = QgsProject.instance().layoutManager().layoutByName('Mise en page automatique MapCEN (Carto de localisation générale)').clone()

        self.dlg.graphicsView.setScene(self.layout_carto_generale)

    #     self.highlight_features()
    #
    #
    # # function that does the work of highlighting selected features
    # def highlight_features(self):
    #
    #     # récupérer la couche active dans QGIS
    #     layer = iface.activeLayer()
    #
    #     # créer une expression de filtre basée sur les IDs des entités sélectionnées
    #     expression = "insee_dep IN ('{}')".format("','".join(self.dlg.comboBox_2.currentText()[0:2]))
    #
    #     # récupérer le symbole de remplissage de la couche
    #     symbol = layer.renderer().symbol().clone()
    #
    #     # définir l'opacité du symbole de remplissage des entités sélectionnées à 0 (entièrement transparent)
    #     symbol.symbolLayer(0).setOpacity(0)
    #
    #     # créer une règle de rendu pour les entités sélectionnées
    #     rule_selected = QgsRuleBasedRenderer.Rule(symbol, filterExpression=expression)
    #
    #     # créer une règle de rendu par défaut pour toutes les autres entités
    #     rule_default = QgsRuleBasedRenderer.Rule(layer.renderer().symbol().clone())
    #
    #     # créer un objet de rendu basé sur les règles de rendu créées
    #     renderer = QgsRuleBasedRenderer(rule_default)
    #     renderer.addChildRule(rule_selected)
    #
    #     # mettre à jour le rendu de la couche avec le rendu modifié
    #     layer.setRenderer(renderer)
    #
    #     # forcer le rafraîchissement de l'affichage de la couche dans QGIS
    #     layer.triggerRepaint()