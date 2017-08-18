#!/usr/bin/python

# This script reads git commit log in format %s from stdin and reads a check list with JIRA ticket number from plain text file to verify if target commit from text file is included in commit log
# commit log starting with '#' will be ignored


import re, sys, time

pattern = re.compile(r'GATEWAY-(\d+)|GW-(\d+)')

class ansi_color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'
    PADDING = 9


# ticket number string vs True/False
target_tickets = {}

def read_check_list(file_name):
    f = open(file_name)
    ticket_map = {}
    for line in f:
        ticket_map[line[:-1]] = False
    f.close()

    return ticket_map

if __name__ == '__main__':
    extra_tickets = {}


    target_tickets = read_check_list(sys.argv[1])

    for git_commit_log_subject in sys.stdin:
        if len(git_commit_log_subject) > 1 :
            # Skip comment
            if git_commit_log_subject[0] == '#':
                continue

            # Try to match jira ticket pattern
            match = pattern.search(git_commit_log_subject)
            
            if match is not None:
                match_groups = match.groups()
                ticket_number = match_groups[0] if match_groups[0] is not None else match_groups[1]

                if target_tickets.has_key(ticket_number):
                    target_tickets[ticket_number] = True
                else:
                    extra_tickets[ticket_number] = True


    # Output result
    print 'Check Result -'
    sorted_tickets = sorted(target_tickets)
    for ticket in sorted_tickets:
        if target_tickets[ticket]:
            print ansi_color.GREEN + 'GATEWAY-%s' % ticket + ' Check' + ansi_color.END
        else:
            print ansi_color.RED + 'GATEWAY-%s' % ticket + ' Missing' + ansi_color.END

    print ''
    print 'Additional Tickets Covered - '
    sorted_tickets = sorted(extra_tickets)
    for ticket in sorted_tickets:
        print ansi_color.YELLOW + 'GATEWAY-%s' % ticket + ansi_color.END
