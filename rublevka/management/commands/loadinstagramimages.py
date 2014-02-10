#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evgeniy Pokidov
# @Date:   2013-11-26 12:36:20
# @Email:  pokidovea@gmail.com
# @Last modified by:   pokidovea
# @Last Modified time: 2013-11-26 14:55:59

from django.core.management.base import BaseCommand
from rublevka.models import InstagramAccount, InstagramImage
from instagram.client import InstagramAPI
from django.conf import settings


class Command(BaseCommand):

    can_import_settings = True
    requires_model_validation = True

    def handle(self, *args, **options):

        api = InstagramAPI(access_token=settings.INSTAGRAM_ACCESS_TOKEN)

        for account in InstagramAccount.objects.all():
            latest_image = account.latest_image

            if latest_image:
                recent_media, next = api.user_recent_media(user_id=account.instagram_id, min_id=latest_image.instagram_id)
            else:
                recent_media, next = api.user_recent_media(user_id=account.instagram_id)

            for media in recent_media:
                media_id = media.id.split('_')[0]
                if not latest_image or media_id != str(latest_image.instagram_id):
                    InstagramImage.objects.create(account=account,
                                                  instagram_id=media_id,
                                                  instagram_link=media.link,
                                                  url=media.images['standard_resolution'].url)
