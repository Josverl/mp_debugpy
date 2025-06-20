_on_fire = False

class Door:
    def __init__(self):
        self.is_open = False
        self.is_locked = False

    def open(self):
        if self.is_locked:
            print("Critical error: Cannot open: Door is locked.")
        else:
            self.is_open = True
            print("Door is now open.")

    def close(self):
        self.is_open = False
        print("Door is now closed.")

    def lock(self):
        if self.is_open:
            print("Cannot lock: Door is open.")
        else:
            self.is_locked = True
            print("Door is now locked.")

    def unlock(self):
        self.is_locked = False
        print("Door is now unlocked.")


class DoorController:
    def __init__(self, door):
        self.door = door

    def toggle(self):
        if self.door.is_open:
            self.door.close()
        else:
            self.door.open()


def check_door_status(door):
    return "open" if door.is_open else "closed"

def operate_door(controller):
    controller.toggle()
    return check_door_status(controller.door)



