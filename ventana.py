# Archivo que sirve para para todos los demás proyectos

from SistemaFotovoltaico_ui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
import math

demandaPotencia = 0
demandaEnergia = 0
cargas = 0

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args,  **kwargs)
        self.setupUi(self)

        """ Primera Interfaz """
        self.ocultarLabels()
        self.pushButton_generarTabla.clicked.connect(self.generarTabla)

        # Layout principal
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Índices de las celdas que queremos bloquear: columnas 0 y 5, y fila 0
        blocked_cells = [(0, col) for col in range(self.tableWidget.columnCount())]

        # Bloquear celdas especificadas
        for row, col in blocked_cells:
            item = self.tableWidget.item(row, col)
            
            if item is None:  # Si la celda no tiene item, crear uno vacío
                item = QTableWidgetItem("")
                self.tableWidget.setItem(row, col, item)

            # Bloquear la edición de la celda
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # Centrar texto de las columnas
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item:  # Verificar que la celda no esté vacía
                    item.setTextAlignment(Qt.AlignCenter)
  
        # Ajustar el tamaño de la primera columna
        self.tableWidget.setColumnWidth(0, 222)

        # Ocultar la tabla
        for col in range(6):
            self.tableWidget.setColumnHidden(col, True)

        # Verificar que las celdas de los datos tengan números
        self.tableWidget.cellChanged.connect(self.verificarNumeroEnCelda)

        # Verificar que las celdas estén llenes y posteriormente realizar el calculo de demanda
        self.pushButton_calcularDemanda.clicked.connect(self.verificarCeldasLlenas)

        # Banco de baterías
        self.pushButton_calcularBaterias.clicked.connect(self.bancoDeBaterias)

        # Sistema Fotovoltaico
        self.pushButton_calcularSistemaFotovoltaico.clicked.connect(self.sistemaFotovoltaico)

        """ Segunda Interfaz """
        self.lineEdit_eficienciaInversor.textChanged.connect(lambda: self.verificarNumeroInterfaz2(1))
        self.lineEdit_voltajeSistema.textChanged.connect(lambda: self.verificarNumeroInterfaz2(2))
        self.lineEdit_autonomia.textChanged.connect(lambda: self.verificarNumeroInterfaz2(3))
        self.lineEdit_capacidadBateria.textChanged.connect(lambda: self.verificarNumeroInterfaz2(4))
        self.lineEdit_factorDescarga.textChanged.connect(lambda: self.verificarNumeroInterfaz2(5))
        self.lineEdit_voltajeBateria.textChanged.connect(lambda: self.verificarNumeroInterfaz2(6))

        self.pushButton_calcularBancoBaterias.clicked.connect(self.calcularBancoBaterias)
        self.pushButton_volver.clicked.connect(self.ocultarLabels)

        """ Tercera Interfaz """
        self.lineEdit_eficienciaInversor_2.textChanged.connect(lambda: self.verificarNumeroInterfaz3(1))
        self.lineEdit_eficienciaBateria.textChanged.connect(lambda: self.verificarNumeroInterfaz3(2))
        self.lineEdit_horasSolarPico.textChanged.connect(lambda: self.verificarNumeroInterfaz3(3))
        self.lineEdit_corrientePicoModulo.textChanged.connect(lambda: self.verificarNumeroInterfaz3(4))
        self.lineEdit_voltajeSistema_2.textChanged.connect(lambda: self.verificarNumeroInterfaz3(5))
        self.lineEdit_voltajeModulo.textChanged.connect(lambda: self.verificarNumeroInterfaz3(6))
        self.lineEdit_cortocircuitoModulo.textChanged.connect(lambda: self.verificarNumeroInterfaz3(7))

        self.pushButton_calcularSistemaPaneles.clicked.connect(self.calcularSistemaPaneles)
        self.pushButton_volver_2.clicked.connect(self.ocultarLabels)


    """ PRIMERA INTERFAZ """

    def generarTabla(self):
        global cargas

        self.ocultarLabels()
        self.label_enunciado_2.setVisible(True)

        # Obtener el texto del input
        str_numeroCargas = self.spinBox_numeroCargas.text()

        # Convertir texto a lista de números
        cargas = int(str_numeroCargas) + 1
        # Configurar tabla
        self.tableWidget.setRowCount(cargas)
        self.tableWidget.setColumnCount(6)
        
        # Mostrar tabla excepto la columna 5 (watts consumidos)
        for col in range (5):
            self.tableWidget.setColumnHidden(col, False)

        # Mostrar botón de calcular Demanda
        self.pushButton_calcularDemanda.setVisible(True)

    def ocultarLabels(self):
        """ Primera Interfaz """
        self.stackedWidget.setCurrentIndex(0)
        # Ocultar columa 5 (watts consumidos)
        self.tableWidget.setColumnHidden(5, True)

        # Ocultar los labels y botones
        self.label_enunciado_2.setVisible(False)
        self.label_titulo2.setVisible(False)
        self.label_titulo3.setVisible(False)
        self.label_rta1.setVisible(False)
        self.label_rta2.setVisible(False)
        self.label_wattsTotales.setVisible(False)
        self.label_consumoPromedio.setVisible(False)
        self.pushButton_calcularDemanda.setVisible(False)
        self.pushButton_calcularBaterias.setVisible(False)
        self.pushButton_calcularSistemaFotovoltaico.setVisible(False)

    # Función para validar que los valores sean números
    def verificarNumeroEnCelda(self, row, col):
        item = self.tableWidget.item(row, col)
        if item != "":
            # Centra el texto en la celda cambiada
            item.setTextAlignment(Qt.AlignCenter)

        # Ignorar la validación si la celda está en la primera columna (nombre de las cargas)
        if col == 0:
            return
    
        # Obtenemos el texto de la celda
        valor_celda = self.tableWidget.item(row, col).text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if valor_celda != "":
                valor = float(valor_celda)

                if valor <= 0 or (col == 3 and valor <= 0) or (col == 3 and valor > 24) or (col == 4 and valor <= 0) or (col == 4 and valor > 7):
                    QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
                    # Restablecemos el valor de la celda
                    self.tableWidget.item(row, col).setText("")

        except ValueError:
            # Si hay un error en la conversión (no es un número válido), mostramos un mensaje de error
            QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
            # Restablecemos el valor de la celda
            self.tableWidget.item(row, col).setText("")

    def verificarCeldasLlenas(self):
        # Verificar si todas las celdas (excepto la última columna) tienen valores
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                if col != 5:  # Excluimos la columna 5 de la validación
                    item = self.tableWidget.item(row, col)
                    if item is None or item.text() == "":
                        # Si alguna celda (excepto la columna 5) está vacía, mostrar un mensaje de error y salir de la función
                        QMessageBox.warning(self, "Error", "Por favor, complete todas las celdas antes de calcular.")
                        return 
        
        # Si todas las celdas (excepto la columna 5) tienen valores, calcular la demanda
        self.calcularDemanda()

    def calcularDemanda(self):
        self.mostrarItemsOcultosInterfaz1()

        global demandaPotencia, demandaEnergia
        demandaPotencia = 0
        demandaEnergia = 0
        
        # Recorremos todas las filas de la tabla
        for row in range(1, self.tableWidget.rowCount()):
            str_cantidad = self.tableWidget.item(row, 1)  # Columna 1 (Cantidad)
            str_watts = self.tableWidget.item(row, 2)  # Columna 2 (Watts)
            str_horasDeUso = self.tableWidget.item(row, 3)  # Columna 2 (Watts)
            str_diasDeUso = self.tableWidget.item(row, 4)  # Columna 2 (Watts)

            cantidad = float(str_cantidad.text())
            watts = float(str_watts.text())
            horasDeUso = float(str_horasDeUso.text())
            diasDeUso = float(str_diasDeUso.text())

            wattsTotales = cantidad * watts
            # Watts consumidos
            wattsConsumidos = wattsTotales * horasDeUso * diasDeUso / 7
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(round(wattsConsumidos))))

            # Bloquear la edición de la celda
            item = self.tableWidget.item(row, 5)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            # Demanda de energía
            demandaEnergia += wattsConsumidos
            self.label_consumoPromedio.setText(str(round(demandaEnergia)) + " Wh")

            # Demanda de potencia
            demandaPotencia += wattsTotales
            self.label_wattsTotales.setText(str(round(demandaPotencia)))

    def mostrarItemsOcultosInterfaz1(self):
        # Mostrar nuevamente la columna 5, de los Watts consumidos
        self.tableWidget.setColumnHidden(5, False)

        # Mostrar los labels y botones
        self.label_titulo2.setVisible(True)
        self.label_titulo3.setVisible(True)
        self.label_rta1.setVisible(True)
        self.label_rta2.setVisible(True)
        self.label_wattsTotales.setVisible(True)
        self.label_consumoPromedio.setVisible(True)
        self.pushButton_calcularBaterias.setVisible(True)
        self.pushButton_calcularSistemaFotovoltaico.setVisible(True)

    """ SEGUNDA INTERFAZ """

    def bancoDeBaterias(self):
        self.stackedWidget.setCurrentIndex(1)
        self.label_tituloAh.setVisible(False)
        self.label_tituloWh.setVisible(False)
        self.label_tituloParalelo.setVisible(False)
        self.label_tituloSerie.setVisible(False)
        self.label_tituloTotal.setVisible(False)
        self.label_capacidadTotalAh.setVisible(False)
        self.label_capacidadTotalWh.setVisible(False)
        self.label_bateriasSerie.setVisible(False)
        self.label_bateriasParalelo.setVisible(False)
        self.label_bateriasTotales.setVisible(False)

    def verificarNumeroInterfaz2(self, numeroEntrada):
        if numeroEntrada == 1:
            entrada = self.lineEdit_eficienciaInversor.text()
        elif numeroEntrada == 2:
            entrada = self.lineEdit_voltajeSistema.text()
        elif numeroEntrada == 3:
            entrada = self.lineEdit_autonomia.text()
        elif numeroEntrada == 4:
            entrada = self.lineEdit_capacidadBateria.text()
        elif numeroEntrada == 5:
            entrada = self.lineEdit_factorDescarga.text()
        else:
            entrada = self.lineEdit_voltajeBateria.text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if entrada != "":
                valor = float(entrada)

                if valor <= 0:
                    self.setearEntradaInterfaz2(numeroEntrada)
                elif (numeroEntrada == 1 or numeroEntrada == 5) and valor > 100:
                    self.setearEntradaInterfaz2(numeroEntrada)
        except ValueError:
            self.setearEntradaInterfaz2(numeroEntrada)
    
    def setearEntradaInterfaz2(self, entrada):
        QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        if entrada == 1:
            self.lineEdit_eficienciaInversor.setText("")
        elif entrada == 2:
            self.lineEdit_voltajeSistema.setText("")
        elif entrada == 3:
            self.lineEdit_autonomia.setText("")
        elif entrada == 4:
            self.lineEdit_capacidadBateria.setText("")
        elif entrada == 5:
            self.lineEdit_factorDescarga.setText("")
        else:
            self.lineEdit_voltajeBateria.setText("")

    def calcularBancoBaterias(self):
        try:
            eficienciaInversor = float(self.lineEdit_eficienciaInversor.text()) / 100
            voltajeSistema = float(self.lineEdit_voltajeSistema.text())
            autonomia = float(self.lineEdit_autonomia.text())
            capacidadBateria = float(self.lineEdit_capacidadBateria.text())
            factorDescarga = float(self.lineEdit_factorDescarga.text()) / 100
            voltajeBateria = float(self.lineEdit_voltajeBateria.text())
        except:
            QMessageBox.warning(self, "Error", "Por favor, ingrese todos los valores.")
            return

        ah_dia = demandaEnergia / eficienciaInversor / voltajeSistema
        bateriasParalelo = math.ceil((ah_dia * autonomia) / (capacidadBateria * factorDescarga))
        bateriasSerie = math.ceil(voltajeSistema / voltajeBateria)
        bateriasTotales = bateriasParalelo * bateriasSerie

        self.label_capacidadTotalAh.setText(str(round(ah_dia)))
        self.label_capacidadTotalWh.setText(str(round(demandaEnergia)))
        self.label_bateriasParalelo.setText(str(bateriasParalelo))
        self.label_bateriasSerie.setText(str(bateriasSerie))
        self.label_bateriasTotales.setText(str(bateriasTotales))
        self.mostrarItemsOcultosInterfaz2()
    
    def mostrarItemsOcultosInterfaz2(self):
        # Mostrar los labels
        self.label_tituloAh.setVisible(True)
        self.label_tituloWh.setVisible(True)
        self.label_tituloParalelo.setVisible(True)
        self.label_tituloSerie.setVisible(True)
        self.label_tituloTotal.setVisible(True)
        self.label_capacidadTotalAh.setVisible(True)
        self.label_capacidadTotalWh.setVisible(True)
        self.label_bateriasSerie.setVisible(True)
        self.label_bateriasParalelo.setVisible(True)
        self.label_bateriasTotales.setVisible(True)

    """ TERCERA INTERFAZ """

    def sistemaFotovoltaico(self):
        self.stackedWidget.setCurrentIndex(2)
        self.label_tituloPanelesSerie.setVisible(False)
        self.label_tituloPanelesParalelo.setVisible(False)
        self.label_tituloTotalPaneles.setVisible(False)
        self.label_tituloCapacidadControlador.setVisible(False)
        self.label_tituloPotenciaInversor.setVisible(False)
        self.label_tituloVoltajeInversor.setVisible(False)
        self.label_panelesSerie.setVisible(False)
        self.label_panelesParalelo.setVisible(False)
        self.label_totalPaneles.setVisible(False)
        self.label_capacidadControlador.setVisible(False)
        self.label_potenciaInversor.setVisible(False)
        self.label_voltajeInversor.setVisible(False)

    def verificarNumeroInterfaz3(self, numeroEntrada):
        if numeroEntrada == 1:
            entrada = self.lineEdit_eficienciaInversor_2.text()
        elif numeroEntrada == 2:
            entrada = self.lineEdit_eficienciaBateria.text()
        elif numeroEntrada == 3:
            entrada = self.lineEdit_horasSolarPico.text()
        elif numeroEntrada == 4:
            entrada = self.lineEdit_corrientePicoModulo.text()
        elif numeroEntrada == 5:
            entrada = self.lineEdit_voltajeSistema_2.text()
        elif numeroEntrada == 6:
            entrada = self.lineEdit_voltajeModulo.text()
        else:
            entrada = self.lineEdit_cortocircuitoModulo.text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if entrada != "":
                valor = float(entrada)

                if valor <= 0:
                    self.setearEntradaInterfaz3(numeroEntrada)
                elif (numeroEntrada == 1 or numeroEntrada == 2) and valor > 100:
                    self.setearEntradaInterfaz3(numeroEntrada)
        except ValueError:
            self.setearEntradaInterfaz3(numeroEntrada)

    def setearEntradaInterfaz3(self, entrada):
        QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        if entrada == 1:
            self.lineEdit_eficienciaInversor_2.setText("")
        elif entrada == 2:
            self.lineEdit_eficienciaBateria.setText("")
        elif entrada == 3:
            self.lineEdit_horasSolarPico.setText("")
        elif entrada == 4:
            self.lineEdit_corrientePicoModulo.setText("")
        elif entrada == 5:
            self.lineEdit_voltajeSistema_2.setText("")
        elif entrada == 6:
            self.lineEdit_voltajeModulo.setText("")
        else:
            self.lineEdit_cortocircuitoModulo.setText("")

    def calcularSistemaPaneles(self):
        try:
            eficienciaInversor = float(self.lineEdit_eficienciaInversor_2.text()) / 100
            eficienciaBateria = float(self.lineEdit_eficienciaBateria.text()) / 100
            horasSolarPico = float(self.lineEdit_horasSolarPico.text())
            corrientePicoModulo = float(self.lineEdit_corrientePicoModulo.text())
            voltajeSistema = float(self.lineEdit_voltajeSistema_2.text())
            voltajeModulo = float(self.lineEdit_voltajeModulo.text())
            cortocircuitoModulo = float(self.lineEdit_cortocircuitoModulo.text())
        except:
            QMessageBox.warning(self, "Error", "Por favor, ingrese todos los valores.")
            return

        ah_dia = demandaEnergia / eficienciaInversor / voltajeSistema
        amperesPicoArreglo = ah_dia / eficienciaBateria / horasSolarPico
        panelesParalelo = math.ceil(amperesPicoArreglo / corrientePicoModulo)
        panelesSerie = math.ceil(voltajeSistema / voltajeModulo)
        panelesTotales = panelesParalelo * panelesSerie
        capacidadControlador = math.ceil(1.25 * cortocircuitoModulo * panelesParalelo)
        while(capacidadControlador % 10 != 0):
            capacidadControlador += 1

        self.label_panelesSerie.setText(str(panelesSerie))
        self.label_panelesParalelo.setText(str(panelesParalelo))
        self.label_totalPaneles.setText(str(panelesTotales))
        self.label_capacidadControlador.setText(str(capacidadControlador) + " A")
        self.label_potenciaInversor.setText(str(round(demandaPotencia)) + " W")
        self.label_voltajeInversor.setText(str(int(voltajeSistema)) + " V")
        self.mostrarItemsOcultosInterfaz3()
    
    def mostrarItemsOcultosInterfaz3(self):
        # Mostrar los labels
        self.label_tituloPanelesSerie.setVisible(True)
        self.label_tituloPanelesParalelo.setVisible(True)
        self.label_tituloTotalPaneles.setVisible(True)
        self.label_tituloCapacidadControlador.setVisible(True)
        self.label_tituloPotenciaInversor.setVisible(True)
        self.label_tituloVoltajeInversor.setVisible(True)
        self.label_panelesSerie.setVisible(True)
        self.label_panelesParalelo.setVisible(True)
        self.label_totalPaneles.setVisible(True)
        self.label_capacidadControlador.setVisible(True)
        self.label_potenciaInversor.setVisible(True)
        self.label_voltajeInversor.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()