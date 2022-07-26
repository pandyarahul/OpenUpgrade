# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tools import cloc
from odoo.addons.base.tests import test_cloc

class TestClocFields(test_cloc.TestClocCustomization):

    def test_fields_from_import_module(self):
        """
            Check that custom computed fields installed with an imported module
            is counted as customization
        """
        self.env['ir.module.module'].create({
            'name': 'imported_module',
            'state': 'installed',
            'imported': True,
        })
        f1 = self.create_field('x_imported_field')
        self.create_xml_id('imported_module', 'import_field', f1)
        cl = cloc.Cloc()
        cl.count_customization(self.env)
        self.assertEqual(cl.code.get('imported_module', 0), 1, 'Count fields with xml_id of imported module')

    def test_fields_from_studio(self):
        # Studio module does not exist at this stage, so we simulate it
        # Check for existing module in case the test run on an existing database
        if not self.env['ir.module.module'].search([('name', '=', 'studio_customization')]):
            self.env['ir.module.module'].create({
                'author': 'Odoo',
                'imported': True,
                'latest_version': '13.0.1.0.0',
                'name': 'studio_customization',
                'state': 'installed',
                'summary': 'Studio Customization',
            })

        f1 = self.create_field('x_field_count')
        self.create_xml_id('studio_customization', 'field_count', f1)
        cl = cloc.Cloc()
        cl.count_customization(self.env)
        self.assertEqual(cl.code.get('studio_customization', 0), 0, "Don't count field generated by studio")
        f2 = self.create_field('x_studio_manual_field')
        self.create_xml_id('studio_customization', 'manual_field', f2)
        cl = cloc.Cloc()
        cl.count_customization(self.env)
        self.assertEqual(cl.code.get('studio_customization', 0), 1, "Count manual field created via studio")

    def test_fields_module_name(self):
        """
            Check that custom computed fields installed with an imported module
            is counted as customization
        """
        self.env['ir.module.module'].create({
            'name': 'imported_module',
            'state': 'installed',
            'imported': True,
        })
        f1 = self.create_field('x_imported_field')
        self.create_xml_id('imported_module', 'import_field', f1)
        self.create_xml_id('__export__', 'import_field', f1)

        sa = self.create_server_action("Test imported double xml_id")
        self.create_xml_id("imported_module", "first", sa)
        self.create_xml_id("__export__", "second", sa)
        cl = cloc.Cloc()
        cl.count_customization(self.env)
        self.assertEqual(cl.code.get('imported_module', 0), 3)
