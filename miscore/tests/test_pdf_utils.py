from decimal import Decimal

from django.test import TestCase

from miscore.pdf_utils import render_curriculum_pdf
from miscore.tests.utils import create_base_data


class PdfUtilsTest(TestCase):
    def test_render_curriculum_pdf_returns_pdf_bytes(self):
        data = create_base_data()
        curriculum = data["curriculum"]

        items = curriculum.listcourse_items.select_related("course").order_by(
            "semester_no",
            "course__code",
        )

        pdf_bytes = render_curriculum_pdf(
            curriculum=curriculum,
            items=items,
            total_active_credits=Decimal("3.0"),
        )

        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 100)