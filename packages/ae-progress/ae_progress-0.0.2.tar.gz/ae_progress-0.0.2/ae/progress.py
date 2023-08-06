"""
display progress of long running processes
==========================================

This module is simplifying the display of progress messages on
the command console/shell of your OS for long running processes.


Basic Usage
-----------

Create an instance of the :class:`Progress` for each process/thread your application spawns::

    from ae.core import SubApp
    from ae.progress import Progress

    app = SubApp(...)
    ...
    progress = Progress(app, ...)

Now you can call the :meth:`~Progress.next` method within your
long running process on each processed item/percentage::

    while process_is_not_finished:
        ...
        progress.next()

Optionally you can request to print an end-message by
calling the :meth:`~Progress.finished` method of your :class:`Progress` instance as
soon as the process is finished::

    ...
    progress.finished()

The above code snippets are printing a start message to your console at the instantiation of :class:`Progress`.
Then every call of the method :meth:`~Progress.next` will print the next message and finally the method
:meth:`~Progress.finished` will print an end message.

To use the integrated error counter and output pass the message of any occurring error to the argument
:paramref:`~Progress.next.error_msg` of :meth:`~Progress.next`.


Progress Instantiation
----------------------

The :paramref:`first argument <Progress.app_base>` expects the
instance of the application class (either :class:`~ae.core.AppBase`,
:class:`~ae.core.SubApp` or :class:`~ae.console.ConsoleApp`) that spawns the process.

The next three arguments are configuring a run or item counter. And the other arguments
may be used to adopt the format of the displayed messages to your needs.


Process run counter
...................

Depending on the type of process you want to show progress differently, e.g. on each processed item or
after passing a certain percentage value and either as incrementing or decrementing number.
For that :class:`Progress` provides a counter which
can be flexible configured with the arguments :paramref:`~Progress.start_counter` and
:paramref:`~Progress.total_count`.

Specifying only :paramref:`~Progress.start_counter` results in a countdown. e.g. for to
display the number of items waiting to be processed::.

    progress = Progress(app, number_of_items_to_be_processed)

By only specifying :paramref:`~Progress.total_count` you get an incremental process run counter::

    progress = Progress(app, total_count=number_of_items_to_be_processed)

For to display a percentage on the console in 5 percent steps specify :paramref:`~Progress.total_count`
as 100 percent and :paramref:`~Progress.delta` as +5::

    progress = Progress(app, total_count=100, delta=5)


Individual Message Templates
............................

Progress displays 5 types of messages on the console. For to overwrite the generic
default message templates pass them into the following arguments:

* :paramref:`~Progress.start_msg`: start message on process start and class instantiation
* :paramref:`~Progress.nothing_to_do_msg`: nothing-to-do message on process start (class instantiation)
* :paramref:`~Progress.err_msg`: error message on any occurring error (on each call of either :meth:`~Progress.next`
  or :meth:`~Progress.finished`)
* :paramref:`~Progress.next_msg`: next run message (on each call of :meth:`~Progress.next`)
* :paramref:`~Progress.end_msg`: finished message (on call of :meth:`~Progress.finished`)

The following table shows which progress state placeholders you can use in which message type:

+---------------+------------------------------------------+
|  placeholder  |  available in message type               |
+===============+==========================================+
| run_counter   |  start, next, end, error, finished       |
| total_count   |  start, next, end, error, finished       |
| processed_id  |  next, end, error, finished              |
| err_counter   |  next, end, error, finished              |
| err_msg       |  next, end, error, finished              |
+---------------+------------------------------------------+

"""
from typing import Optional

# noinspection PyProtectedMember
from ae.core import AppBase, _logger        # type: ignore      # mypy

__version__ = '0.0.2'


class Progress:
    """ helper class for to easily display progress of long running tasks with several items on the console/log output.
    """
    def __init__(
            self, app_base: AppBase,
            start_counter: int = 0, total_count: int = 0, delta: int = -1,
            # templates for to display messages on process start, run, end, on error if nothing-to-do
            start_msg: str = "", next_msg: Optional[str] = "",
            end_msg: str = "Finished processing of {total_count} having {err_counter} failures:¡{err_msg}!",
            err_msg: str = "{err_counter} errors on processing {total_count} items, current={run_counter}:¡{err_msg}!",
            nothing_to_do_msg: str = ''):
        """ prepare print-outs for a new progress (long running process with incrementing or decrementing item counter).

        :param app_base:            instance of an application class.
        :param start_counter:       process item counter start value.
                                    counter decrements on each call of :meth:`~Progress.next` (if
                                    :paramref:`~Progress.total_count` not specified).
        :param total_count:         number of items that will be processed with an incrementing counter.
                                    By passing a positive integer the process item counter will be incremented
                                    on each call of :meth:`~Progress.next`.
        :param delta:               difference to decrement/increment on each call of :meth:`~Progress.next`.
        :param start_msg:           start message template with placeholders.
        :param next_msg:            next message - if an empty string get passed then a default message
                                    will be provided with placeholders - pass None if you want to suppress the
                                    print-out of a next message.
        :param end_msg:             end message template with placeholders, pass None if you want to suppress the
                                    print-out of an end message (in this case only a new line will be printed).
        :param err_msg:             error message template with placeholders.
        :param nothing_to_do_msg:   message template printed-out if the values of the two arguments
                                    :paramref:`~Progress.start_counter` and :paramref:`~Progress.total_count` are
                                    less or equal to zero.
        """
        self.app_base: AppBase = app_base   #: reference attribute to the used :class:`core.AppBase` instance
        if next_msg == "":
            next_msg = "Processing '{processed_id}': " + \
                       ("left" if start_counter > 0 and total_count == 0 else "item") + \
                       " {run_counter} of {total_count}. {err_counter} errors:¡{err_msg}!"

        def _complete_msg_prefix(msg, pch='#'):
            return (pch in msg and msg) or msg and " " + pch * 3 + "  " + msg or ""

        self._next_msg = _complete_msg_prefix(next_msg)
        self._end_msg = _complete_msg_prefix(end_msg)
        self._err_msg = _complete_msg_prefix(err_msg, '*')

        self._err_counter = 0
        self._run_counter = start_counter - delta  # def=decrementing run_counter
        self._total_count = start_counter
        self._delta = delta
        if total_count > 0:  # incrementing run_counter
            self._run_counter = start_counter
            self._total_count = total_count
            self._delta = abs(delta)
        elif start_counter <= 0:
            if nothing_to_do_msg:
                self.app_base.po(_complete_msg_prefix(nothing_to_do_msg), logger=_logger)
            return  # RETURN -- empty set - nothing to process

        if start_msg:
            self.app_base.po(_complete_msg_prefix(start_msg).format(run_counter=self._run_counter + self._delta,
                                                                    total_count=self._total_count), logger=_logger)

    def next(self, processed_id: str = '', error_msg: str = '', next_msg: str = '', delta: int = 0):
        """ log the processing of the next item of this long-running task.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       pass the error message to display if the next item produced any errors.
        :param next_msg:        message to output (use instance message if not passed/empty).
        :param delta:           delta for decrement/increment process run counter (use instance default if not passed).
        """
        self._run_counter += delta or self._delta
        if error_msg:
            self._err_counter += 1

        params = dict(run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
                      err_counter=self._err_counter, err_msg=error_msg)
        if error_msg and self._err_msg:
            self.app_base.po(self._err_msg.format(**params), logger=_logger)

        if not next_msg:
            next_msg = self._next_msg
        if next_msg:
            # using print_out()/po() with end parameter instead of leading \r will NOT GET DISPLAYED within PyCharm,
            # .. also not with flush - see http://stackoverflow.com/questions/34751441/
            # when-writing-carriage-return-to-a-pycharm-console-the-whole-line-is-deleted
            # .. po('   ', pend, end='\r', flush=True)
            next_msg = '\r' + next_msg
            self.app_base.po(next_msg.format(**params), logger=_logger)

    def finished(self, processed_id: str = '', error_msg: str = ''):
        """ display end of processing for the current item.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       optional error message to display if current items produced any error.
        """
        if error_msg:
            self._err_counter += 1
            if self._end_msg:
                self.app_base.po(self._err_msg.format(
                    run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
                    err_counter=self._err_counter, err_msg=error_msg),
                                 logger=_logger)
        self.app_base.po(self.get_end_message(error_msg=error_msg), logger=_logger)

    def get_end_message(self, processed_id: str = '', error_msg: str = '') -> str:
        """ determine message text for finishing the currently processed item.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       optional error message to display if current items produced any error.
        :return:                message text for to display.
        """
        return self._end_msg.format(
            run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
            err_counter=self._err_counter, err_msg=error_msg)
