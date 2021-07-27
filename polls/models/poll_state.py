from django.db import models


class PollState(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    class Meta:
        db_table = "poll_state"
