##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2023 Comunitea Servicios Tecnológicos S.L. All Rights Reserved
#    Vicente Ángel Gutiérrez <vicente@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import uuid
from datetime import date, datetime, timedelta
from odoo import SUPERUSER_ID, _, api, exceptions, models, fields


class ResUsers(models.Model):

    _inherit = "res.users"

    portal_access_token = fields.Char()
    portal_access_token_expire = fields.Datetime()

    def create_portal_token_access(self):
        for user in self:
            if not user.portal_access_token or user.portal_access_token_expire > datetime.now():
                user.portal_access_token = uuid.uuid4().hex
                user.portal_access_token_expire = datetime.now() + timedelta(days=30)

    def _check_credentials(self, password, env):
        try:
            return super(ResUsers, self)._check_credentials(password, env)

        except exceptions.AccessDenied:
            # Just be sure that parent methods aren't wrong
            users = self.with_user(SUPERUSER_ID).search([("id", "=", self._uid)])
            if not users:
                raise

            if not self.portal_access_token \
                or self.portal_access_token_expire < datetime.now() \
                or self.portal_access_token != password:
                raise
