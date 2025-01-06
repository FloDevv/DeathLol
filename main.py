import time
import logging
import argparse
import urllib3
from overlay import DeathOverlay
from leagueclient import LeagueClient

def parse_args():
    parser = argparse.ArgumentParser(description='Death Detector for League of Legends')
    parser.add_argument('-debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()

def setup_logging(debug_mode):
    if debug_mode:
        handlers = [logging.StreamHandler()]
        level = logging.INFO
    else:
        handlers = []
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

# Prevent SSL warning spam
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    args = parse_args()
    setup_logging(args.debug)

    overlay = DeathOverlay()
    client = LeagueClient()

    if args.debug:
        print("Death detector started in DEBUG mode. Press Ctrl+C to exit.")
    else:
        print("Death detector started. Press Ctrl+C to exit.")

    try:
        while True:
            is_dead = client.get_player_state()
            if is_dead:
                overlay.show_overlay()
            else:
                overlay.hide_overlay()
            overlay.update()
            time.sleep(1.0)

    except KeyboardInterrupt:
        overlay.root.destroy()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        overlay.root.destroy()

if __name__ == "__main__":
    main()
