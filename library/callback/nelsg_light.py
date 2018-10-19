# coding=utf-8
# pylint: disable=I0011,E0401,C0103,C0111,W0212

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import yaml
import copy
from datetime import datetime

try:
    from ansible.utils.color import colorize, hostcolor
    from ansible.plugins.callback import CallbackBase
except ImportError:
    class CallbackBase:
        # pylint: disable=I0011,R0903
        pass

# Fields we will delete from the result
DELETABLE_FIELDS = ['_ansible_verbose_always', '_ansible_no_log']

CHANGED = 'yellow'
UNCHANGED = 'green'

def yaml_serialize(data, indent=0):
    output_data = copy.deepcopy(data)
    for key in output_data.keys():
        if key in DELETABLE_FIELDS:
            del output_data[key]
    return yaml.safe_dump(output_data, encoding='utf-8', allow_unicode=True, default_flow_style=False)

class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'nelsg_light'

    def v2_playbook_on_task_start(self, task, is_conditional):
        # pylint: disable=I0011,W0613
        self._open_section(task.get_name(), task.get_path())
        self._task_level += 1

    def _open_section(self, section_name, path = None):
        if self._display.verbosity > 1:
            if path:
                self._emit_line("{}".format(path))
        self.task_start_preamble = "{} ...".format(
            section_name)
        sys.stdout.write(self.task_start_preamble)


    def v2_playbook_on_handler_task_start(self, task):
        self._emit_line("triggering handler | %s " % task.get_name().strip())

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # pylint: disable=I0011,W0613,W0201
        self._task_level = 0

        if 'exception' in result._result:
            exception_message = "An exception occurred during task execution."
            if self._display.verbosity < 3:
                # extract just the actual error message from the exception text
                error = result._result['exception'].strip().split('\n')[-1]
                msg = exception_message + \
                    "To see the full traceback, use -vvv. The error was: %s" % error
            else:
                msg = exception_message + \
                    "The full traceback is:\n" + \
                    result._result['exception'].replace('\n', '')

                self._emit_line(msg, color='red')

        self._emit_line("FAILED", color='red')
        self._emit_line(yaml_serialize(result._result), color='cyan')

    def v2_on_file_diff(self, result):

        if result._task.loop and 'results' in result._result:
            for res in result._result['results']:
                if 'diff' in res and res['diff'] and res.get('changed', False):
                    diff = self._get_diff(res['diff'])
                    if diff:
                        self._emit_line(diff)

        elif 'diff' in result._result and \
                result._result['diff'] and \
                result._result.get('changed', False):
            diff = self._get_diff(result._result['diff'])
            if diff:
                self._emit_line(diff)

    def v2_runner_on_ok(self, result):
        # pylint: disable=I0011,W0201,
        self._clean_results(result._result, result._task.action)

        self._clean_results(result._result, result._task.action)

        if result._task.action in ('include', 'include_role'):
            sys.stdout.write("\b\b\b\b    \n")
            return

        self._task_level = 0
        msg, color = self._changed_or_not(result._result)

        if result._task.loop and self._display.verbosity > 0 and 'results' in result._result:
            for item in result._result['results']:
                msg, color = self._changed_or_not(item)
                item_msg = "%s - item=%s" % (msg, self._get_item(item))
                self._emit_line("%s" %
                                (item_msg), color=color)
        else:
            self._emit_line("%s" %
                            (msg), color=color)
        self._handle_warnings(result._result)

        if (
            self._display.verbosity > 0 or
            '_ansible_verbose_always' in result._result
        ) and not '_ansible_verbose_override' in result._result:
            self._emit_line(yaml_serialize(result._result), color=color)

        result._preamble = self.task_start_preamble

    def _changed_or_not(self, result):
        if result.get('changed', False):
            msg = "CHANGED"
            color = CHANGED
        else:
            msg = "SUCCESS"
            color = UNCHANGED

        return [msg, color]

    def _emit_line(self, lines, color='normal'):

        if self.task_start_preamble is None:
            self._open_section("system")

        if self.task_start_preamble.endswith(" ..."):
            sys.stdout.write("\b\b\b\b | ")
            self.task_start_preamble = " "

        for line in lines.splitlines():
            self._display.display(line, color=color)

    def v2_runner_on_unreachable(self, result):
        self._task_level = 0
        self._emit_line("UNREACHABLE!: %s", color=CHANGED)

    def v2_runner_on_skipped(self, result):
        self._task_level = 0

        self._emit_line("SKIPPED", color='cyan')

    def v2_playbook_on_include(self, included_file):
        self._open_section("system")

        msg = 'included: %s for %s' % \
            (included_file._filename, ", ".join(
                [h.name for h in included_file._hosts]))
        self._emit_line(msg, color='cyan')

    def v2_playbook_on_stats(self, stats):
        pass

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self._task_level = 0
        self.task_start_preamble = None
        # python2 only
        try:
            reload(sys).setdefaultencoding('utf8')
        except:
            pass


if __name__ == '__main__':
    unittest.main()
