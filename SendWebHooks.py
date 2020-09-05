import glob
import os
import xml.etree.cElementTree as Et
import pymsteams


def main():
    test_files_directory = os.path.join(os.getcwd(), "Tests")

    test_files = glob.glob(os.path.join(test_files_directory, "*.xml"))

    for test_file in test_files:
        teams_webhook_card = pymsteams.connectorcard(WEBHOOK_URL)

        teams_webhook_card.title("Nightly UI Tests Run")

        teams_webhook_card.summary("Nightly UI Tests Run")

        teams_webhook_card.color("0076D7")

        message_section = pymsteams.cardsection()

        message_section.activityTitle(os.path.basename(test_file))

        message_section.activitySubtitle("Test results: ")

        document = Et.parse(test_file)

        test_suits = document.getroot()

        for test_suit in test_suits:
            message_section.addFact("Test Suit: ", test_suit.attrib['name'])
            message_section.addFact("Errors: ", test_suit.attrib['errors'])
            message_section.addFact("Failures: ", test_suit.attrib['failures'])
            message_section.addFact("Time: ", test_suit.attrib['time'])
            message_section.addFact("Tests: ", test_suit.attrib['tests'])

            for test_case in test_suit:
                message_section.addFact("TestCase: ", test_case.attrib['name'])
                message_section.addFact("Time: ", test_case.attrib['time'])

                for test_case_failure in test_case:
                    message_section.addFact("Failures: ", f'{test_case_failure.text}')

        teams_webhook_card.addSection(message_section)

        teams_webhook_card.printme()

        teams_webhook_card.send()


if __name__ == '__main__':
    main()
