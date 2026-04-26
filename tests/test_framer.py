from smr2modbus.framer import TelegramFramer
import unittest


class FramerTests(unittest.TestCase):
    def test_frames_across_chunks(self) -> None:
        framer = TelegramFramer()
        chunk1 = "/HEADER\n1-0:31.7.0(016*A)\n"
        chunk2 = "1-0:51.7.0(000*A)\n!A32F\n"

        out1 = framer.feed(chunk1)
        self.assertEqual(out1, [])

        out2 = framer.feed(chunk2)
        self.assertEqual(len(out2), 1)
        self.assertIn("!A32F", out2[0])


if __name__ == "__main__":
    unittest.main()
