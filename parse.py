import optparse
from app import process_data, sync_tickets

def main():
    parser = optparse.OptionParser()
    parser.add_option("--find-duplicates", action="store_true", dest="find_duplicates")
    parser.add_option("--sync-tickets", action="store_true", dest="sync_tickets")
    parser.add_option("--title", dest="title")
    parser.add_option("--platform", dest="platform")
    parser.add_option("--threshold", type=float, dest="threshold")

    options, args = parser.parse_args()

    if options.find_duplicates:
        response = process_data(options.title, options.platform, options.threshold)
        print(response)

    elif options.sync_tickets:
        response = sync_tickets()
        print(response)

if __name__ == '__main__':
    main()
