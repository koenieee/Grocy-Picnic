class GrocyPicnicProduct():
    grocy_id = ""
    grocy_name = ""
    grocy_img_id = ""
    grocy_weight = ""
    grocy_id_stock = ""
    picnic_id = ""

    def __init__(self, picnic_id: str, grocy_id: str, grocy_name:str, grocy_img_id: str, grocy_weight: str, grocy_id_stock: str):
        self.picnic_id = picnic_id
        self.grocy_id = grocy_id
        self.grocy_name = grocy_name
        self.grocy_img_id = grocy_img_id
        self.grocy_weight = grocy_weight
        self.grocy_id_stock = grocy_id_stock

    def __repr__(self):
        return """
        grocy_id:       """+self.grocy_id+"""
        grocy_name:     """+self.grocy_name+"""
        grocy_img_id:   """+self.grocy_img_id+"""
        grocy_weight:   """+self.grocy_weight+"""
        grocy_id_stock: """+self.grocy_id_stock+"""
        picnic_id:      """+self.picnic_id+"""
        """