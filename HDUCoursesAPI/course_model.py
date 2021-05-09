class Course:
    def __init__(self):
        self.status = ''
        self.title = ''
        self.credit = 0.0
        self.method = ''
        self.property = ''
        self.teacher = ''
        self.class_id = ''
        self.time_info: list[dict] = []
        self.week_info = {}
        self.location = []
        self.academic = ''
        self.other = []
