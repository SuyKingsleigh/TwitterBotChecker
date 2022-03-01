class Mention:
    # mention_id
    # since_id
    # checked_at
    def __init__(self, mention_id, since_id, checked_at=None, id=None):
        self.mention_id = mention_id
        self.since_id = since_id
        self.id = id
        self.checked_at = checked_at
