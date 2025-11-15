

class FixParser:
    def parse(self, msg: str):
        parts = msg.split("|")

        data = {}

        for field in parts:
            tag, value = field.split("=")
            data[tag] = value

        #check for missing tags
        if "35" not in data:
            raise ValueError("Missing message type (tag 35)")
        
        if data["35"] == "D":
            for tag in ["55","54","38"]:
                if tag not in data:
                    raise ValueError(f"Missing required tag {tag}")
        
        if data.get("40") == "2" and "44" not in data:
            raise ValueError("Limit order requires tag 44 (price)")

        return data
    
