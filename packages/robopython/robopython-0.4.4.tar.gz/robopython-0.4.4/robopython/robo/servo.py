class Servo(object):

    def __init__(self, name, ble, mqtt, protocol, default_topic, id_num, action_id):
        self.is_connected = 0
        self.name = name
        self.id = id_num
        self.action_id = action_id
        self.action_status = None
        self.BLE = ble
        self.MQTT = mqtt
        self.protocol = protocol
        self.default_topic = default_topic

    def connected(self):
        self.is_connected = 1
        
    def disconnected(self):
        self.is_connected = 0

    def set_angle(self, angle, topic=None):
        assert type(angle) is int, "Angle must be an integer"
        packet_size = 0x04
        command_id = 0x51
        payload_size = 0x02
        module_id = self.id-1
        command = bytearray([packet_size, command_id, payload_size, module_id, angle])

        if topic is None:
            topic = self.default_topic

        if angle < 0 or angle > 255:
            print("Angle must be between 0-255")
            return

        if self.is_connected == 1:
            if self.protocol == "BLE":
                self.BLE.write_to_robo(self.BLE.write_uuid, command)
                return
            if self.protocol == "MQTT":
                command = self.MQTT.get_mqtt_cmd([command_id, payload_size, module_id, angle])
                self.MQTT.publish(topic, command)
                return
        print(self.name + " is NOT Connected!")

    def get_encoder(self):
        pass

    def action_complete(self, id, cmd_status):
        self.action_status = cmd_status

    def check_action(self):
        value = self.action_status
        if self.action_status is None:
            return
        self.action_status = None
        return value

