# from django.db import models

# # IPs block list model of the honeypot.
# class BlockedIP(models.Model):
#     ip = models.GenericIPAddressField()
#     # The time the IP was blocked.
#     blocked_at = models.DateTimeField(auto_now_add=True)
#     # The time the IP will be unblocked.
#     # This is calculated as blocked_at + block_period.
#     unblocked_at = models.DateTimeField()
#     # The block period in seconds.
#     block_period = models.PositiveIntegerField(default=60)

#     def __str__(self):
#         return self.ip

#     def save(self, *args, **kwargs):
#         # Calculate the unblocked_at field.
#         self.unblocked_at = self.blocked_at + datetime.timedelta(seconds=self.block_period)
#         super().save(*args, **kwargs)

#     def is_blocked(self):
#         # Check if the IP is still blocked.
#         return timezone.now() < self.unblocked_at

#     class Meta:
#         verbose_name = 'Blocked IP'
#         verbose_name_plural = 'Blocked IPs'
#         ordering = ['-blocked_at']
