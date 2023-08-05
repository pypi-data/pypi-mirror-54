import difflib
import collections
import prompt_toolkit
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, Window, WindowAlign
from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings


Action = collections.namedtuple('Action', ['name', 'key', 'action'])


def prompt(text, title='', actions=[], **kwargs):
    """A simple and extensible prompt helper routine

    :param text: Text to be printed before the prompt, it can be formatted text
    :type  text: str or FormattedText
    :param title: Title to be shown in a bottom bar
    :type  title: str
    :param actions: A list of Actions as defined in `Action`.
    :type  actions: [Action]
    :param kwargs: kwargs to prompt_toolkit application class
    """
    assert(isinstance(actions, list))
    assert(type(title) == str)

    kb = KeyBindings()

    for action in actions:
        kb.add(action.key)(action.action)

    prompt_toolkit.print_formatted_text(FormattedText(text))

    root_container = HSplit([

        Window(
            wrap_lines=True,
            height=1,
            align=WindowAlign.LEFT,
            always_hide_cursor=True,
            style='bg:ansiblack fg:ansiwhite',
            content=FormattedTextControl(
                focusable=False,
                text=HTML(' '.join(
                    "{a.name}<yellow>[{a.key}]</yellow>".format(a=a)
                    for a in actions
                ))
            )
        )] +
        ([
            Window(
                height=1, align=WindowAlign.LEFT,
                always_hide_cursor=True, style='bold fg:ansipurple bg:ansiwhite',
                content=FormattedTextControl(focusable=False, text=title))
        ] if title else [])
    )

    app = Application(
        layout=Layout(root_container),
        key_bindings=kb,
        **kwargs)
    app.run()


def diffshow(texta, textb, title='', namea='a', nameb='b', actions=[]):
    """Show the difference of texta and textb with a prompt.

    :param texta: From text
    :type  texta: str
    :param textb: To text
    :type  textb: str
    """
    assert(isinstance(actions, list))
    assert(isinstance(texta, str))
    assert(isinstance(textb, str))

    # diffs = difflib.unified_diff(
            # str(texta).splitlines(keepends=True),
            # str(textb).splitlines(keepends=True),
            # fromfile=namea, tofile=nameb)

    diffs = difflib.ndiff(
            str(texta).splitlines(keepends=True),
            str(textb).splitlines(keepends=True),)

    raw_text = list(diffs) + [
        ("bg:ansiblack fg:ansipurple", "^^^^^^^^^\ndiff from\n"),
        "----- {namea}\n".format(namea=namea),
        "+++++ {nameb}\n".format(nameb=nameb),]

    formatted_text = list(map(lambda line:
        # match line values
        isinstance(line, tuple) and line or
        line.startswith('@') and ('fg:violet bg:ansiblack', line) or
        line.startswith('+') and ('fg:ansigreen bg:ansiblack', line) or
        line.startswith('-') and ('fg:ansired bg:ansiblack', line) or
        line.startswith('?') and ('fg:ansiyellow bg:ansiblack', line) or
        ('fg:ansiwhite', line), raw_text))

    prompt(
        title=title,
        text=formatted_text,
        actions=actions)


def diffdict(dicta, dictb, namea='a', nameb='b'):
    """
    Compute the difference of two dictionaries.

    :param dicta: Base dictionary
    :type  dicta: dict
    :param dictb: Dictionary with the differences that the result might add
    :type  dictb: dict
    :param namea: Label to be shown for dictionary a
    :type  namea: str
    :param namea: Label to be shown for dictionary b
    :type  namea: str
    :returns: A dictionary containig the base data of dicta plus data
        from dictb if this was chosen.
    :rtype:  return_type
    """

    rdict = dict()

    options = {
        "add": False,
        "reject": False,
        "split": False,
        "quit": False,
        "add_all": False,
        "cancel": False,
    }

    def reset():
        for k in options:
            options[k] = False

    def oset(event, option, value):
        options[option] = value
        event.app.exit(0)

    actions = [
        Action(
            name='Add all', key='a', action=lambda e: oset(e, "add_all", True)),
        Action(
            name='Split', key='s', action=lambda e: oset(e, "split", True)),
        Action(
            name='Reject', key='n', action=lambda e: oset(e, "reject", True)),
        Action(
            name='Quit', key='q', action=lambda e: oset(e, "quit", True)),
        Action(
            name='Cancel', key='c', action=lambda e: oset(e, "cancel", True)),
    ]

    keys = [k for k in sorted(set(dicta) | set(dictb))
            if not dicta.get(k) == dictb.get(k) and dictb.get(k)]

    texta = "\n".join(
            "{k}: {v}".format(k=k, v=dicta.get(k, '')) for k in sorted(keys)
            ) + "\n"
    textb = "\n".join(
            "{k}: {v}".format(k=k, v=dictb.get(k, '')) for k in sorted(keys)
            ) + "\n"

    diffshow(
        texta=texta, textb=textb,
        title='GENERAL DIFFERENCE',
        namea=namea,
        nameb=nameb,
        actions=actions)

    if options["cancel"] or options['quit']:
        return dict()
    elif options["add_all"]:
        rdict.update(dicta)
        rdict.update(dictb)
        return rdict
    elif options["split"]:
        reset()

    actions = [
        Action(name='Add', key='y', action=lambda e: oset(e, "add", True)),
    ] + actions

    for key in keys:

        if options["add_all"]:
            rdict[key] = dictb.get(key, dicta.get(key))
            continue

        diffshow(
            texta=str(dicta.get(key, '')) + "\n",
            textb=str(dictb.get(key, '')) + "\n",
            title='Key: {0}'.format(key),
            namea=namea,
            nameb=nameb,
            actions=actions)

        if options["cancel"]:
            return dict()
        elif options["add"]:
            rdict[key] = dictb.get(key, dicta.get(key))
        elif options["quit"]:
            break

        if not options["add_all"]:
            reset()

    return rdict
