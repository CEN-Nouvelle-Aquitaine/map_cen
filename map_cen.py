# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapCEN
                                 A QGIS plugin
 Mise en page automatique (ajout de la légende, d'une barre d'échelle, de la flèche du nord, d'un titre) d'un projet QGIS.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-05-20
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Romain Montillet
        email                : r.montillet@cen-na.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from PyQt5 import *

from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.PyQt.QtXml import QDomDocument
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .map_cen_dialog import MapCENDialog
import os.path
import urllib
import csv
import io
import processing

from datetime import date

class Calcul(QThread):
    # crée un nouveau signal pour indiquer la fin du thread
    finduthread = pyqtSignal()

    # ========================================================================
    def __init__(self, parent=None):
        super(Calcul, self).__init__(parent)

    # ========================================================================
    def run(self):
        # tempo de 5 secondes pour l'exemple
        time.sleep(5)
        # émet le signal de fin du thread
        self.finduthread.emit()

class MapCEN:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MapCEN_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&MapCEN')
        self.dlg = MapCENDialog()
        self.plugin_path = os.path.dirname(__file__)

        # self.dlg.commandLinkButton.clicked.connect(self.actualisation_emprise)
    
        #
        # liste_couches_fonciercen =[]
        #
        # url_open = urllib.request.urlopen("https://raw.githubusercontent.com/CEN-Nouvelle-Aquitaine/fluxcen/main/flux.csv")
        # self.colonnes_flux = csv.DictReader(io.TextIOWrapper(url_open, encoding='utf8'), delimiter=';')
        #
        # for row in self.colonnes_flux:
        #     if row['categorie'] == 'fonciercen':
        #         liste_couches_fonciercen.append(row['Nom_couche_plugin'])
        #
        # self.dlg.comboBox.addItems(liste_couches_fonciercen)


        self.dlg.commandLinkButton.clicked.connect(self.chargement_qpt)

        self.dlg.commandLinkButton_2.clicked.connect(self.initialisation)
        self.dlg.commandLinkButton_4.clicked.connect(self.actualisation_emprise)
        self.dlg.commandLinkButton_5.clicked.connect(self.ouverture_composeur)
        self.dlg.commandLinkButton_6.clicked.connect(self.export)

        # self.default_project_scale = self.iface.mapCanvas().scale()
        # print("echelle par défaut à l'initilaisation du plugin", self.default_project_scale)

        self.dlg.graphicsView.scale(2.1,2.1)


        self.dlg.commandLinkButton_2.setEnabled(True)
        self.dlg.lineEdit.setEnabled(False)
        self.dlg.commandLinkButton_4.setEnabled(False)
        self.dlg.commandLinkButton_5.setEnabled(False)
        self.dlg.commandLinkButton_6.setEnabled(False)


        # self.dlg.comboBox_2.setEnabled(False)



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapCEN', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/map_cen/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&MapCEN'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def initialisation(self):

        self.dlg.commandLinkButton_2.setEnabled(False)


        managerAU = QgsApplication.authManager()
        self.k = managerAU.availableAuthMethodConfigs().keys()
        # print( k )
        if len(list(self.k)) == 0:
            QMessageBox.question(iface.mainWindow(), u"Attention !", "Veuillez ajouter une entrée de configuration d'authentification dans QGIS pour accéder aux flux CEN-NA sécurisés par un mot de passe", QMessageBox.Ok)


        uri = ['https://opendata.cen-nouvelle-aquitaine.org/geoserver/fonciercen/wfs?VERSION=1.0.0&TYPENAME=fonciercen:site_gere_poly&SRSNAME=EPSG:4326&authcfg=', list(self.k)[0], '&request=GetFeature']
        uri = ''.join(uri)

        self.listes_sites_MFU = []
        self.vlayer = QgsVectorLayer(uri, "Sites gérés CEN-NA", "WFS")
        # layer.setScaleBasedVisibility(True)
        # layer.setMaximumScale(10000)
        # layer.setMinimumScale(50000)
        self.vlayer.loadNamedStyle(self.plugin_path + '/styles_couches/' + self.vlayer.name() + '.qml')
        self.vlayer.triggerRepaint()

        for p in self.vlayer.getFeatures():
            self.listes_sites_MFU.append(str(p.attributes()[2]))

        # self.dlg.comboBox_2.addItems(listes_sites_MFU)

        completer = QCompleter(self.listes_sites_MFU)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.dlg.lineEdit.setCompleter(completer)







        project = QgsProject.instance()

        mises_en_page = []

        for filename in glob.glob(self.plugin_path + "/mises_en_pages/*.qpt"):
            mises_en_page.append(filename)


        for i, filename in enumerate(mises_en_page):
            nom_fichier = os.path.basename(filename)
            print(nom_fichier)
            self.dlg.comboBox.addItem(nom_fichier)

        # self.dlg.tableWidget.setRowCount(len(mises_en_page))
        # self.dlg.tableWidget.setColumnCount(1)
        # self.dlg.tableWidget.setColumnWidth(0, 300)
        # self.dlg.tableWidget.setHorizontalHeaderLabels(["Modèles de mises en page"])
        # self.dlg.tableWidget.verticalHeader().setVisible(False)
        #
        # for i, filename in enumerate(mises_en_page):
        #     nom_fichier = os.path.basename(filename)
        #     item = QTableWidgetItem(nom_fichier)
        #     self.dlg.tableWidget.setItem(i, 0, item)



        self.ajout_couches()

    def ajout_couches(self):

        #on divise niveau d'échelle par 3 lorsque le projet est vide pour compenser le zoom d'échelle * 4 dans la fonction "actualisation_emprise" (un peu à l'arrache mais bon...)
        self.iface.mapCanvas().zoomScale(round((iface.mapCanvas().scale()/1.2)))


        ### -------------------- Chargement des sites fonciercen ---------------------- ###


        # url_open = urllib.request.urlopen("https://raw.githubusercontent.com/CEN-Nouvelle-Aquitaine/fluxcen/main/flux.csv")
        # colonnes_flux = csv.DictReader(io.TextIOWrapper(url_open, encoding='utf8'), delimiter=';')
        #
        # for row in colonnes_flux:
        #     nom_technique = [row["nom_technique"] for row in colonnes_flux if row['Nom_couche_plugin'] == self.dlg.comboBox.currentText()]
        #
        # uri = ['https://opendata.cen-nouvelle-aquitaine.org/geoserver/fonciercen/wfs?VERSION=1.0.0&TYPENAME=',nom_technique[0], '&SRSNAME=EPSG:4326&authcfg=', list(k)[0], '&request=GetFeature']
        # uri = ''.join(uri)

        uri = ['https://opendata.cen-nouvelle-aquitaine.org/geoserver/fonciercen/wfs?VERSION=1.0.0&TYPENAME=fonciercen:mfu_cenna&SRSNAME=EPSG:4326&authcfg=', list(self.k)[0], '&request=GetFeature']
        uri = ''.join(uri)

        # méthode plus rapide pour charger layer que QgsProject.instance().addMapLayer(layer) :
        if not QgsProject.instance().mapLayersByName("Parcelles CEN NA en MFU"):
            self.layer = iface.addVectorLayer(uri, "Parcelles CEN NA en MFU", "WFS")

        if not self.layer:
            # QMessageBox.question(iface.mainWindow(), u"Erreur !", "Impossible de charger la couche %s, veuillez contacter le pôle DSI !" % self.dlg.comboBox.currentText(), QMessageBox.Ok)
            QMessageBox.question(iface.mainWindow(), u"Erreur !", "Impossible de charger la couche 'Parcelles CEN NA en MFU', veuillez contacter le pôle DSI !", QMessageBox.Ok)

        self.layer.loadNamedStyle(self.plugin_path + '/styles_couches/mfu_cenna.qml')
        self.layer.triggerRepaint()

        if not QgsProject.instance().mapLayersByName("Sites gérés CEN-NA"):
            QgsProject.instance().addMapLayer(self.vlayer)
        if not self.vlayer:
            QMessageBox.question(iface.mainWindow(), u"Erreur !", "Impossible de charge la couche %s, veuillez contacter le pôle DSI !" % self.dlg.lineEdit.text(), QMessageBox.Ok)

        self.depts_NA = iface.addVectorLayer(
            "https://opendata.cen-nouvelle-aquitaine.org/administratif/wfs?VERSION=1.0.0&TYPENAME=administratif:departement&SRSNAME=EPSG:4326&request=GetFeature",
            "Département", "WFS")

        single_symbol_renderer = self.depts_NA.renderer()

        symbol = single_symbol_renderer.symbol()
        symbol.setColor(QColor.fromRgb(255, 0, 0, 0))

        # more efficient than refreshing the whole canvas, which requires a redraw of ALL layers
        self.depts_NA.triggerRepaint()

        # self.alti_aquitaine = iface.addRasterLayer("url=https://opendata.cen-nouvelle-aquitaine.org/geoserver/fond_carto/wms&service=WMS+Raster&version=1.0.0&crs=EPSG:2154&format=image/png&layers=fond_carto_alti_aquitaine&styles", "fond_carto_alti_aquitaine", "wms")
        # self.alti_limousin = iface.addRasterLayer("url=https://opendata.cen-nouvelle-aquitaine.org/geoserver/fond_carto/wms&service=WMS+Raster&version=1.0.0&crs=EPSG:2154&format=image/png&layers=fond_carto_alti_limousin&styles", "fond_carto_alti_limousin", "wms")
        # self.alti_pc = iface.addRasterLayer("url=https://opendata.cen-nouvelle-aquitaine.org/geoserver/fond_carto/wms&service=WMS+Raster&version=1.0.0&crs=EPSG:2154&format=image/png&layers=fond_carto_alti_pc&styles", "fond_carto_alti_pc", "wms")

        self.activation_boutons()

    def activation_boutons(self):

        # self.dlg.comboBox_2.setEnabled(True)
        self.dlg.lineEdit.setEnabled(True)
        self.dlg.commandLinkButton_4.setEnabled(True)
        self.dlg.commandLinkButton_5.setEnabled(True)
        self.dlg.commandLinkButton_6.setEnabled(True)


    def actualisation_emprise(self):

        ### -------------------- Choix et ajout des fonds de carte ---------------------- ###

        if self.dlg.radioButton.isChecked() == True:
            tms = 'type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}'
            self.fond = QgsRasterLayer(tms, "Google Sat'", 'wms')

            if not QgsProject.instance().mapLayersByName("Google Sat'"):
                QgsProject.instance().addMapLayer(self.fond)
            else:
                print("Le fond de carte Google Sat' est déjà chargé")

            fond_carte = QgsProject.instance().mapLayersByName("Google Sat'")[0]

        else :
            for lyr in QgsProject.instance().mapLayers().values():
                if lyr.name() == "Google Sat'":
                    QgsProject.instance().removeMapLayers([lyr.id()])


        if self.dlg.radioButton_2.isChecked() == True:

            tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'
            self.fond = QgsRasterLayer(tms, 'OSM', 'wms')

            if not QgsProject.instance().mapLayersByName("OSM"):
                QgsProject.instance().addMapLayer(self.fond)
            else:
                print("Le fond de carte Google Sat' est déjà chargé")

            fond_carte = QgsProject.instance().mapLayersByName("OSM")[0]

        else :
            for lyr in QgsProject.instance().mapLayers().values():
                if lyr.name() == "OSM":
                    QgsProject.instance().removeMapLayers([lyr.id()])


        if self.dlg.radioButton_3.isChecked() == True:

            uri = 'url=https://opendata.cen-nouvelle-aquitaine.org/geoserver/fond_carto/wms?service=WMS+Raster&version=1.0.0&crs=EPSG:2154&format=image/png&layers=SCAN25TOUR_PYR-JPEG_WLD_WM&styles'
            self.fond = QgsRasterLayer(uri, "SCAN25 IGN", "wms")

            if not QgsProject.instance().mapLayersByName("SCAN25 IGN"):
                QgsProject.instance().addMapLayer(self.fond)
            else:
                print("Le fond de carte SCAN25 IGN est déjà chargé")

            fond_carte = QgsProject.instance().mapLayersByName("SCAN25 IGN")[0]

        else :
            for lyr in QgsProject.instance().mapLayers().values():
                if lyr.name() == "SCAN25 IGN":
                    QgsProject.instance().removeMapLayers([lyr.id()])


        # Ordre des couches dans gestionnaires couches : fond de carte sous les autres couches
        root = QgsProject.instance().layerTreeRoot()
        fond_carte = root.findLayer(fond_carte.id())
        myClone = fond_carte.clone()
        parent = fond_carte.parent()
        parent.insertChildNode(-1, myClone)
        parent.removeChildNode(fond_carte)


        # ### Zoom sur emprise du site CEN selectionné:

        if self.dlg.lineEdit.text() in self.listes_sites_MFU:

            self.vlayer.selectByExpression("\"nom_site\"= '" + self.dlg.lineEdit.text() + "'")

            iface.mapCanvas().zoomToSelected(self.vlayer)

            QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(2154))

            ##On change légèrement l'échelle de visualisation du project en la diminuant légèrement car sinon zoom trop important lorsque zoomtoextent(layer) dans composeur d'impression
            self.iface.mapCanvas().zoomScale(round((iface.mapCanvas().scale()*1.2)))

            rules = (
                ('Site CEN sélectionné', "is_selected()", 'red'),
            )

            # create a new rule-based renderer
            symbol = QgsSymbol.defaultSymbol(self.vlayer.geometryType())
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
                print(symbol_layer)
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
            self.vlayer.setRenderer(renderer)
            # refresh the layer on the map canvas
            self.vlayer.triggerRepaint()

            expr = "\"nom_site\"= '" + self.dlg.lineEdit.text() + "'"
            self.layer.setSubsetString(expr)

            self.mise_en_page()

        else:
            QMessageBox.question(iface.mainWindow(), u"Nom de site invalide", "Renseigner un nom de site CEN-NA valide !", QMessageBox.Ok)


    def mise_en_page(self):

        # QgsProject.instance().layerTreeRoot().findLayer(self.vlayer.id()).setItemVisibilityChecked(False)

        ## Ajout de la mise en page au composeur de carte:

        project = QgsProject.instance()
        manager = project.layoutManager()
        layout_name = 'Automatic layout 1'
        layouts_list = manager.printLayouts()
        # Just 4 debug
        # remove any duplicate layouts
        for self.layout in layouts_list:
            if self.layout.name() == layout_name:
                manager.removeLayout(self.layout)
            #     reply = QMessageBox.question(None, (u'Delete layout...'),
            #                                  (
            #                                      u"There's already a layout named '%s'\nDo you want to delete it?")
            #                                  % layout_name,
            #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            #     if reply == QMessageBox.No:
            #         return
            #     else:
            #         manager.removeLayout(layout)
            #         print((u"Previous layout names '%s' removed... ") % layout_name)

        self.layout = QgsPrintLayout(project)
        self.layout.initializeDefaults()
        # manager.addLayout(layout)
        self.layout.setName(layout_name)


        ## Add map to layout
        print("Adding map")
        self.my_map1 = QgsLayoutItemMap(self.layout)

        # Charger une carte vide
        self.my_map1.setRect(20, 20, 20, 20)

        self.my_map1.setLayers([self.layer, self.fond])


        # Mettre le canvas courant comme emprise
        self.my_map1.setExtent(iface.mapCanvas().extent())

        # Position de la carte dans le composeur
        self.my_map1.attemptMove(QgsLayoutPoint(5, 23, QgsUnitTypes.LayoutMillimeters))

        #on dimensionne le rendu de la carte (pour référence la page totale est une page A4 donc 297*210)
        self.my_map1.attemptResize(QgsLayoutSize(185, 182, QgsUnitTypes.LayoutMillimeters))

        self.my_map1.refresh()

        self.my_map1.setBackgroundColor(QColor(255, 255, 255, 255))
        self.my_map1.setFrameEnabled(True)
        self.layout.addLayoutItem(self.my_map1)

        self.my_map1.setId("carte_principale")
        # print(self.my_map1.id())

        # --- create map item 2 (shapefile, raster 2, basemap)

        my_map2 = QgsLayoutItemMap(self.layout)
        my_map2.setRect(20, 20, 20, 20)
        my_map2.setPos(213, 28)
        my_map2.setFrameEnabled(False)

        my_map2.setLayers([self.vlayer, self.depts_NA])

        ## Ajustement de l'emprise de la couche depts_CEN-NA au CRS 2154 :

        crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")

        # recherche du CRS du projet pour réaliser transformation (normalement 2154):
        crsDest = QgsCoordinateReferenceSystem(QgsCoordinateReferenceSystem("EPSG:2154"))
        transformContext = QgsProject.instance().transformContext()
        xform = QgsCoordinateTransform(crsSrc, crsDest, transformContext)

        # forward transformation: src -> dest
        extent = xform.transform(self.depts_NA.extent())


        my_map2.setExtent(extent)
        my_map2.setScale(30000000)

        my_map2.attemptMove(QgsLayoutPoint(213, 28, QgsUnitTypes.LayoutMillimeters))
        my_map2.attemptResize(QgsLayoutSize(63, 63, QgsUnitTypes.LayoutMillimeters))

        self.layout.addLayoutItem(my_map2)


        ## Ajout de la legende :
        print((u"Adding legend"))

        legend = QgsLayoutItemLegend(self.layout)
        # legend.setTitle('Legende')
        legend.adjustBoxSize()
        legend.setFrameEnabled(False)
        legend.setAutoUpdateModel(False)

        root = QgsLayerTree()
        root.addLayer(self.layer).setUseLayerName(False)
        root.addLayer(self.layer).setName("Types de maîtrise")

        legend.updateLegend()

        legend.setLegendFilterByMapEnabled(True)
        self.layout.addItem(legend)
        legend.setLinkedMap(self.my_map1)

        layer_to_remove = self.fond
        legend.model().rootGroup().removeLayer(layer_to_remove)

        legend.attemptMove(QgsLayoutPoint(200, 93, QgsUnitTypes.LayoutMillimeters))

        # legend.setColumnCount(3)

        legend.setColumnCount(0)
        legend.setEqualColumnWidth(True)
        legend.setSplitLayer(True)


        # for legendLyr in iface.mapCanvas().layers():
        #     if legendLyr.name() == "Parcelles CEN NA en MFU":
        #         renderer = legendLyr.renderer()
        #         myRenderer = renderer.clone()
        #         idx = 0
        #         for cat in myRenderer.categories():
        #             if len(cat.label()) >= 35:
        #                 nom_item = cat.label()[:35] + '*' + cat.label()[35:]
        #             else:
        #                 nom_item = cat.label()
        #             idx += 1
        #             myRenderer.updateCategoryLabel(idx, nom_item)
        #         legendLyr.setRenderer(myRenderer)
        #         legendLyr.triggerRepaint()


        legend.setWrapString("*")

        # layer_to_remove = QgsProject().instance().mapLayersByName("Google Sat'")[0]
        # legend = [i for i in self.layout.items() if isinstance(i, QgsLayoutItemLegend)][0]
        # legend.model().rootGroup().removeLayer(layer_to_remove)

        legend.adjustBoxSize()

        self.layout.refresh()



        ## Ajout d'un titre à la mise en page
        title = QgsLayoutItemLabel(self.layout)
        self.layout.addLayoutItem(title)
        titre = str("Maîtrise foncière sur le site : " + self.dlg.lineEdit.text() + " (" + self.vlayer.selectedFeatures()[0]["codesite"] + ")")
        title.setText(titre)
        title.setFont(QFont("Calibri", 16, QFont.Bold))
        title.adjustSizeToText()
        title.attemptMove(QgsLayoutPoint(4.2, 5.8, QgsUnitTypes.LayoutMillimeters))
        title.adjustSizeToText()
        self.layout.addItem(title)


        ## Ajout du logo CEN NA en haut à gauche de la page
        layoutItemPicture = QgsLayoutItemPicture(self.layout)
        layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
        layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
        layoutItemPicture.setPicturePath(self.plugin_path + '/logo_cenna.jpg')

        # dim_image_original = [250, 84]
        # new_dim = [i * 0.15 for i in dim_image_original]
        layoutItemPicture.attemptMove(QgsLayoutPoint(218, 5, QgsUnitTypes.LayoutMillimeters))
        layoutItemPicture.attemptResize(QgsLayoutSize(720,249, QgsUnitTypes.LayoutPixels))

        self.layout.addLayoutItem(layoutItemPicture)


        ## Ajout de l'échelle à la mise en page
        print((u"Adding scale bar"))
        scalebar = QgsLayoutItemScaleBar(self.layout)
        scalebar.setStyle('Single Box')
        scalebar.setLinkedMap(self.my_map1)
        scalebar.applyDefaultSize()
        scalebar.applyDefaultSettings()
        scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
        scalebar.setUnitsPerSegment(scalebar.unitsPerSegment() / 1000)
        scalebar.setUnitLabel('km')
        scalebar.update()
        self.layout.addLayoutItem(scalebar)
        scalebar.attemptMove(QgsLayoutPoint(226,173, QgsUnitTypes.LayoutMillimeters))
        # scalebar.setFixedSize(QgsLayoutSize(50, 20))

        # ajout de la fleche du Nord
        print((u"Add north arrow"))
        north = QgsLayoutItemPicture(self.layout)
        north.setPicturePath(self.plugin_path + "/NorthArrow_02.svg")
        self.layout.addLayoutItem(north)
        north.attemptResize(QgsLayoutSize(8.4, 12.5, QgsUnitTypes.LayoutMillimeters))
        north.attemptMove(QgsLayoutPoint(208,172, QgsUnitTypes.LayoutMillimeters))

        # ajout de la date, l'auteur, source etc...
        date_du_jour = date.today().strftime("%d/%m/%Y")

        info = ["Réalisation : " + "DSI / CEN Nouvelle-Aquitaine (" + date_du_jour + ")"]
        credit_text = QgsLayoutItemLabel(self.layout)
        credit_text.setText(info[0])
        credit_text.setFont(QFont("Calibri", 11))
        credit_text.adjustSizeToText()
        self.layout.addLayoutItem(credit_text)
        credit_text.attemptMove(QgsLayoutPoint(200, 200, QgsUnitTypes.LayoutMillimeters))


        info2 = ["Source: IGN (fond de carte), IGN (Admin Express), cadastre ETALAB, FoncierCEN"]
        credit_text2 = QgsLayoutItemLabel(self.layout)
        credit_text2.setText(info2[0])
        credit_text2.setFont(QFont("Calibri", 9))
        credit_text2.setItemRotation(-90)
        credit_text2.adjustSizeToText()
        self.layout.addLayoutItem(credit_text2)
        credit_text2.attemptMove(QgsLayoutPoint(191, 204, QgsUnitTypes.LayoutMillimeters))


        surf_parcelles_site_selectionne = self.layer.aggregate(QgsAggregateCalculator.Sum, "contenance")
        surf_ha = surf_parcelles_site_selectionne[0]/10000
        info3 = "Surface totale maîtrisée sur le site : " + str(surf_ha) + " ha."
        credit_text3 = QgsLayoutItemLabel(self.layout)
        credit_text3.setText(info3)
        credit_text3.setFont(QFont("Calibri", 14))
        credit_text3.adjustSizeToText()
        self.layout.addLayoutItem(credit_text3)
        credit_text3.attemptMove(QgsLayoutPoint(10.5, 13.5, QgsUnitTypes.LayoutMillimeters))


        # Finally add layout to the project via its manager
        manager.addLayout(self.layout)

        self.zoom_to_layer()


    def ouverture_composeur(self):

        ###  -------------------- Automatisation de la mise en page ----------------------- ###

        iface.openLayoutDesigner(self.layout)

        #### Pour ajouter deuxieme carte au composer d'impression:
        ##https://gis.stackexchange.com/questions/331723/display-two-different-maps-with-different-layers-in-one-layout-in-pyqgis-proble


    def zoom_to_layer(self):

        self.layout2 = QgsProject.instance().layoutManager().layoutByName("Automatic layout 1").clone()
        self.dlg.graphicsView.setScene(self.layout2)


    def export(self):

        # dossier_sauvegarde = QFileDialog.getExistingDirectory()
        #
        # exporter.exportToPdf(f'"{dossier_sauvegarde}/"'), QgsLayoutExporter.PdfExportSettings())


        fileName = QFileDialog.getSaveFileName(None, 'Sauvegarder en png', '', filter='*.png')
        if fileName:
            dossier_sauvegarde = fileName[0]

        exporter = QgsLayoutExporter(self.layout)
        settings = QgsLayoutExporter.ImageExportSettings()
        # The idea is that here you can change setting attributes e.g :
        # settings.cropToContents = True
        # settings.dpi = 150

        result_png = exporter.exportToImage(dossier_sauvegarde, settings)
        print(result_png)  # 0 = Export was successful!


        # result_pdf = exporter.exportToPdf(dossier_sauvegarde, QgsLayoutExporter.PdfExportSettings())
        # print(result_pdf) # 0 = Export was successful!


    def chargement_qpt(self):

        project = QgsProject.instance()

        # current_row = self.dlg.tableWidget.currentRow()
        # current_column = self.dlg.tableWidget.currentColumn()
        # _item = self.dlg.tableWidget.item(current_row, current_column).text()

        for filename in glob.glob(self.plugin_path + "/mises_en_pages/*.qpt"):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                layout = QgsPrintLayout(project)
                layout.initializeDefaults()
                template_content = f.read()
                doc = QDomDocument()
                doc.setContent(template_content)
                layout.loadFromTemplate(doc, QgsReadWriteContext(), True)
                layout.setName(os.path.basename(filename))

                project.layoutManager().addLayout(layout)

        fichier_mise_en_page = self.dlg.comboBox.currentText()

        layout2 = QgsProject.instance().layoutManager().layoutByName(fichier_mise_en_page)

        map_item = layout2.itemById("Carte 1")
        map_item.zoomToExtent(iface.mapCanvas().extent())
        #
        iface.openLayoutDesigner(layout2)



