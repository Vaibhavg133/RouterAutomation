class EOForTimeout(Exception):
    def __init__(self):
        self.msg = 'EOF or Timeout Occured'
    
    def __str__(self):
        return self.msg