from chaveDAO import ChaveDAO
chaveDAO=ChaveDAO()

class Chave:

    def __init__(self, local, usuario_retirada='-', hora_retirada='-', data_retirada='-', usuario_entrega='-', hora_entrega='-', data_entrega='-'):
        self.local = local
        self.usuario_retirada = usuario_retirada
        self.hora_retirada = hora_retirada
        self.data_retirada = data_retirada
        self.usuario_entrega = usuario_entrega
        self.hora_entrega = hora_entrega
        self.data_entrega = data_entrega

    def __str__(self):
        if self.usuario_retirada == '-':
            return "| " + self.local + " |"
        elif self.usuario_retirada != '-' and self.hora_entrega == '-':
            return ("| " + self.local + " | " + self.usuario_retirada + ' | ' + self.data_retirada + ' | ' + self.hora_retirada + ' |')
        else:
            return ("| " + self.local + " | " + self.usuario_retirada + ' | ' + self.data_retirada + ' | Retirada: ' + self.hora_retirada  + ' | Entregue: ' + self.hora_entrega + ' | ' + self.data_entrega + ' | Desvolvedor: ' + self.usuario_entrega + ' |')

    def get_local(self):
        return self.local

    def get_data_retirada(self):
        return self.data_retirada

    def get_usuario_retirada(self):
        return self.usuario_retirada

    def get_hora_retirada(self):
        return self.hora_retirada

    def get_hora_entrega(self):
        return self.hora_entrega

    def get_usuario_entrega(self):
        return self.usuario_entrega

    def get_data_entrega(self):
        return self.data_entrega

    def set_local(self, novo):
        self.local = novo

    def set_data_retirada(self, novo):
        self.data_retirada = novo

    def set_usuario_retirada(self, novo):
        self.usuario_retirada = novo

    def set_hora_retirada(self, novo):
        self.hora_retirada = novo

    def set_hora_entrega(self, novo):
        self.hora_entrega = novo

    def set_usuario_entrega(self, novo):
        self.usuario_entrega = novo
















