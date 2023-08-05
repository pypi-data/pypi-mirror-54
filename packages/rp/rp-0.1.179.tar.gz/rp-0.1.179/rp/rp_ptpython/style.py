from __future__ import unicode_literals

def get_all_ui_styles():
    """
    Return a dict mapping {ui_style_name -> style_dict}.
    """
    return {
        'default': default_ui_style,
        'blue': blue_ui_style,
        # 'inverted_1': inverted_1,
        'lightning': inverted_2,
        'stars': inverted_3,
        'cyan': cyan,
        'aqua': cyan_2,
        'blew':cyan_3,
        'seashell':cyan_4,
        'snailshell':cyan_4__02__02,
        'cobra':cyan_4__02__02__12,#cyan 4 with channels 0 and 2 swapped then channels 0 and 2 swapped then 1 and 2 swapped
        'eggshell':cyan_4__02,
        'jojo':color_1,
        'bizarre':color_2,
        'adventure':color_3,
        'pupper':pupper,
        'clara':clara,
        'emma':emma,
        'dejavu':dejavu,
        'anna':newstyle,
        'spook':sprice,
        'saturn':splicer1,
        'atlantic':splicer2,
        'hot':breeze,
    }

from pygments.token import Token, Keyword, Name, Comment, String, Operator, Number
from pygments.styles import get_style_by_name, get_all_styles
from rp.prompt_toolkit.styles import DEFAULT_STYLE_EXTENSIONS, style_from_dict
from rp.prompt_toolkit.utils import is_windows, is_conemu_ansi

__all__ = (
    'get_all_code_styles',
    'get_all_ui_styles',
    'generate_style',
)


def get_all_code_styles():
    """
    Return a mapping from style names to their classes.
    """
    result = dict((name, get_style_by_name(name).styles) for name in get_all_styles())
    # from rp import mini_terminal_for_pythonista
    # exec(mini_terminal_for_pythonista)
    result['win32'] = win32_code_style
    result['ryan']=ryan_style
    result['clara']=clara_style
    result['viper']=viper_style
    result['stratus']=stratus_style
    result['snape']=snape_style
    return result
from pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator, Punctuation, Generic, Whitespace
"""
The style used in Lovelace interactive learning environment. Tries to avoid
the "angry fruit salad" effect with desaturated and dim colours.
"""
_KW_BLUE='#2838b0'
_NAME_GREEN='#388038'
_DOC_ORANGE='#b85820'
_OW_PURPLE='#a848a8'
_FUN_BROWN='#785840'
_STR_RED='#b83838'
_CLS_CYAN='#287088'
_ESCAPE_LIME='#709030'
_LABEL_CYAN='#289870'
_EXCEPT_YELLOW='#908828'
ryan_style={Token: '',
            Token.Comment: 'italic #888888',
            Token.Comment.Hashbang: '#287088',
            Token.Comment.Multiline: '#888888',
            Token.Comment.Preproc: 'noitalic #289870',
            Token.Comment.PreprocFile: '',
            Token.Comment.Single: '',
            Token.Comment.Special: '',
            # Token.Error: 'bg:#a848a8',
            Token.Escape: '',
            Token.Generic: '',
            Token.Generic.Deleted: '#c02828',
            Token.Generic.Emph: 'italic',
            Token.Generic.Error: '#c02828',
            Token.Generic.Heading: '#666666',
            Token.Generic.Inserted: '#388038',
            Token.Generic.Output: '#666666',
            Token.Generic.Prompt: '#444444',
            Token.Generic.Strong: 'bold',
            Token.Generic.Subheading: '#444444',
            Token.Generic.Traceback: '#2838b0',
            Token.Keyword: '#2838b0 bold',
            Token.Keyword.Constant: 'italic #444444',
            Token.Keyword.Declaration: 'italic',
            Token.Keyword.Pseudo: '',
            Token.Keyword.Reserved: '',
            Token.Keyword.Type: 'italic',
            Token.Literal: '',
            Token.Literal.Date: '',
            Token.Literal.Number: '#444444',
            Token.Literal.Number.Bin: '',
            Token.Literal.Number.Float: '',
            Token.Literal.Number.Hex: '',
            Token.Literal.Number.Integer: '',
            Token.Literal.Number.Integer.Long: '',
            Token.Literal.Number.Oct: '',
            Token.Literal.String: '#b83838',
            Token.Literal.String.Backtick: '',
            Token.Literal.String.Char: '#a848a8',
            Token.Literal.String.Doc: 'italic #b85820',
            Token.Literal.String.Double: '',
            Token.Literal.String.Escape: '#709030',
            Token.Literal.String.Heredoc: '',
            Token.Literal.String.Interpol: 'underline',
            Token.Literal.String.Other: '#a848a8',
            Token.Literal.String.Regex: '#a848a8',
            Token.Literal.String.Single: '',
            Token.Literal.String.Symbol: '',
            Token.Name: '',
            Token.Name.Attribute: '#388038',
            Token.Name.Builtin: '#388038',
            Token.Name.Builtin.Pseudo: 'italic',
            Token.Name.Class: '#287088',
            Token.Name.Constant: '#b85820',
            Token.Name.Decorator: '#287088',
            Token.Name.Entity: '#709030',
            Token.Name.Exception: '#908828',
            Token.Name.Function: '#785840',
            Token.Name.Label: '#289870',
            Token.Name.Namespace: '#289870',
            Token.Name.Other: '',
            Token.Name.Property: '',
            Token.Name.Tag: '#2838b0',
            Token.Name.Variable: '#b04040',
            Token.Name.Variable.Class: '',
            Token.Name.Variable.Global: '#908828',
            Token.Name.Variable.Instance: '',
            Token.Operator: '#666666',
            Token.Operator.Word: '#a848a8',
            Token.Other: '',
            Token.Punctuation: '#888888',
            Token.Text: '',
            Token.Text.Whitespace: '#a89028'}

clara_style={Token: '',
            Token.Comment: 'italic #51a6fb',
            Token.Comment.Hashbang: '#5126db',
            Token.Comment.Multiline: '#51a6fb',
            Token.Comment.Preproc: 'noitalic #3126ff',
            Token.Comment.PreprocFile: '',
            Token.Comment.Single: '',
            Token.Comment.Special: '',
            # Token.Error: 'bg:#7cd1a6',
            Token.Escape: '',
            Token.Generic: '',
            Token.Generic.Deleted: '#00f17b',
            Token.Generic.Emph: 'italic',
            Token.Generic.Error: '#00f17b',
            Token.Generic.Heading: '#2479ce',
            Token.Generic.Inserted: '#003cf0',
            Token.Generic.Output: '#2479ce',
            Token.Generic.Prompt: '#004ca0',
            Token.Generic.Strong: 'bold',
            Token.Generic.Subheading: '#004ca0',
            Token.Generic.Traceback: '#862690',
            Token.Keyword: '#862690 bold',
            Token.Keyword.Constant: 'italic #004ca0',
            Token.Keyword.Declaration: 'italic',
            Token.Keyword.Pseudo: '',
            Token.Keyword.Reserved: '',
            Token.Keyword.Type: 'italic',
            Token.Literal: '',
            Token.Literal.Date: '',
            Token.Literal.Number: '#004ca0',
            Token.Literal.Number.Bin: '',
            Token.Literal.Number.Float: '',
            Token.Literal.Number.Hex: '',
            Token.Literal.Number.Integer: '',
            Token.Literal.Number.Integer.Long: '',
            Token.Literal.Number.Oct: '',
            Token.Literal.String: '#00e690',
            Token.Literal.String.Backtick: '',
            Token.Literal.String.Char: '#7cd1a6',
            Token.Literal.String.Doc: 'italic #00e6bb',
            Token.Literal.String.Double: '',
            Token.Literal.String.Escape: '#0086ff',
            Token.Literal.String.Heredoc: '',
            Token.Literal.String.Interpol: 'underline',
            Token.Literal.String.Other: '#7cd1a6',
            Token.Literal.String.Regex: '#7cd1a6',
            Token.Literal.String.Single: '',
            Token.Literal.String.Symbol: '',
            Token.Name: '',
            Token.Name.Attribute: '#003cf0',
            Token.Name.Builtin: '#003cf0',
            Token.Name.Builtin.Pseudo: 'italic',
            Token.Name.Class: '#5126db',
            Token.Name.Constant: '#00e6bb',
            Token.Name.Decorator: '#5126db',
            Token.Name.Entity: '#0086ff',
            Token.Name.Exception: '#00b1fb',
            Token.Name.Function: '#0091bb',
            Token.Name.Label: '#3126ff',
            Token.Name.Namespace: '#3126ff',
            Token.Name.Other: '',
            Token.Name.Property: '',
            Token.Name.Tag: '#862690',
            Token.Name.Variable: '#00dc9b',
            Token.Name.Variable.Class: '',
            Token.Name.Variable.Global: '#00b1fb',
            Token.Name.Variable.Instance: '',
            Token.Operator: '#2479ce',
            Token.Operator.Word: '#7cd1a6',
            Token.Other: '',
            Token.Punctuation: '#51a6fb',
            Token.Text: '',
            Token.Text.Whitespace: '#00d1ff'}

viper_style={Token: '',
            Token.Comment:                        ' italic      #fb51a6',         
            Token.Comment.Hashbang:               '             #db5126',         
            Token.Comment.Multiline:              '             #fb51a6',         
            Token.Comment.Preproc:                ' noitalic    #ff3126',         
            Token.Comment.PreprocFile:            ' ',                            
            Token.Comment.Single:                 ' ',                            
            Token.Comment.Special:                ' ',                            
            # Token.Error:                          ' bg:         #a67cd1',         
            Token.Escape:                         ' ',                            
            Token.Generic:                        ' ',                            
            Token.Generic.Deleted:                '             #7b00f1',         
            Token.Generic.Emph:                   ' italic',                      
            Token.Generic.Error:                  '             #7b00f1',         
            Token.Generic.Heading:                '             #ce2479',         
            Token.Generic.Inserted:               '             #f0003c',         
            Token.Generic.Output:                 '             #ce2479',         
            Token.Generic.Prompt:                 '             #a0004c',         
            Token.Generic.Strong:                 ' bold',                        
            Token.Generic.Subheading:             '             #a0004c',         
            Token.Generic.Traceback:              '             #908626',         
            Token.Keyword:                        '             #908626 bold',    
            Token.Keyword.Constant:               ' italic      #a0004c',         
            Token.Keyword.Declaration:            ' italic',                      
            Token.Keyword.Pseudo:                 ' ',                            
            Token.Keyword.Reserved:               ' ',                            
            Token.Keyword.Type:                   ' italic',                      
            Token.Literal:                        ' ',                            
            Token.Literal.Date:                   ' ',                            
            Token.Literal.Number:                 '             #a0004c',         
            Token.Literal.Number.Bin:             ' ',                            
            Token.Literal.Number.Float:           ' ',                            
            Token.Literal.Number.Hex:             ' ',                            
            Token.Literal.Number.Integer:         ' ',                            
            Token.Literal.Number.Integer.Long:    ' ',                            
            Token.Literal.Number.Oct:             ' ',                            
            Token.Literal.String:                 '             #9000e6',         
            Token.Literal.String.Backtick:        ' ',                            
            Token.Literal.String.Char:            '             #a67cd1',         
            Token.Literal.String.Doc:             ' italic      #bb00e6',         
            Token.Literal.String.Double:          ' ',                            
            Token.Literal.String.Escape:          '             #ff0086',         
            Token.Literal.String.Heredoc:         ' ',                            
            Token.Literal.String.Interpol:        ' underline',                    
            Token.Literal.String.Other:           '             #a67cd1',         
            Token.Literal.String.Regex:           '             #a67cd1',         
            Token.Literal.String.Single:          ' ',                            
            Token.Literal.String.Symbol:          ' ',                            
            Token.Name:                           ' ',                            
            Token.Name.Attribute:                 '             #f0003c',         
            Token.Name.Builtin:                   '             #f0003c',         
            Token.Name.Builtin.Pseudo:            ' italic',                      
            Token.Name.Class:                     '             #db5126',         
            Token.Name.Constant:                  '             #bb00e6',         
            Token.Name.Decorator:                 '             #db5126',         
            Token.Name.Entity:                    '             #ff0086',         
            Token.Name.Exception:                 '             #fb00b1',         
            Token.Name.Function:                  '             #bb0091',         
            Token.Name.Label:                     '             #ff3126',         
            Token.Name.Namespace:                 '             #ff3126',         
            Token.Name.Other:                     ' ',                            
            Token.Name.Property:                  ' ',                            
            Token.Name.Tag:                       '             #908626',         
            Token.Name.Variable:                  '             #9b00dc',         
            Token.Name.Variable.Class:            ' ',                            
            Token.Name.Variable.Global:           '             #fb00b1',         
            Token.Name.Variable.Instance:         ' ',                            
            Token.Operator:                       '             #ce2479',         
            Token.Operator.Word:                  '             #a67cd1',         
            Token.Other:                          ' ',                            
            Token.Punctuation:                    '             #fb51a6',         
            Token.Text:                           ' ',                            
            Token.Text.Whitespace:                '             #ff00d1'}         


stratus_style={Token: '',
            Token.Comment:                        ' italic      #a6fb51',         
            Token.Comment.Hashbang:               '             #26db51',         
            Token.Comment.Multiline:              '             #a6fb51',         
            Token.Comment.Preproc:                ' noitalic    #26ff31',         
            Token.Comment.PreprocFile:            ' ',                            
            Token.Comment.Single:                 ' ',                            
            Token.Comment.Special:                ' ',                            
            # Token.Error:                          ' bg:         #d1a67c',         
            Token.Escape:                         ' ',                            
            Token.Generic:                        ' ',                            
            Token.Generic.Deleted:                '             #f17b00',         
            Token.Generic.Emph:                   ' italic',                      
            Token.Generic.Error:                  '             #f17b00',         
            Token.Generic.Heading:                '             #79ce24',         
            Token.Generic.Inserted:               '             #3cf000',         
            Token.Generic.Output:                 '             #79ce24',         
            Token.Generic.Prompt:                 '             #4ca000',         
            Token.Generic.Strong:                 ' bold',                        
            Token.Generic.Subheading:             '             #4ca000',         
            Token.Generic.Traceback:              '             #269086',         
            Token.Keyword:                        '             #269086 bold',    
            Token.Keyword.Constant:               ' italic      #4ca000',         
            Token.Keyword.Declaration:            ' italic',                      
            Token.Keyword.Pseudo:                 ' ',                            
            Token.Keyword.Reserved:               ' ',                            
            Token.Keyword.Type:                   ' italic',                      
            Token.Literal:                        ' ',                            
            Token.Literal.Date:                   ' ',                            
            Token.Literal.Number:                 '             #4ca000',         
            Token.Literal.Number.Bin:             ' ',                            
            Token.Literal.Number.Float:           ' ',                            
            Token.Literal.Number.Hex:             ' ',                            
            Token.Literal.Number.Integer:         ' ',                            
            Token.Literal.Number.Integer.Long:    ' ',                            
            Token.Literal.Number.Oct:             ' ',                            
            Token.Literal.String:                 '             #e69000',         
            Token.Literal.String.Backtick:        ' ',                            
            Token.Literal.String.Char:            '             #d1a67c',         
            Token.Literal.String.Doc:             ' italic      #e6bb00',         
            Token.Literal.String.Double:          ' ',                            
            Token.Literal.String.Escape:          '             #86ff00',         
            Token.Literal.String.Heredoc:         ' ',                            
            Token.Literal.String.Interpol:        ' underline',                    
            Token.Literal.String.Other:           '             #d1a67c',         
            Token.Literal.String.Regex:           '             #d1a67c',         
            Token.Literal.String.Single:          ' ',                            
            Token.Literal.String.Symbol:          ' ',                            
            Token.Name:                           ' ',                            
            Token.Name.Attribute:                 '             #3cf000',         
            Token.Name.Builtin:                   '             #3cf000',         
            Token.Name.Builtin.Pseudo:            ' italic',                      
            Token.Name.Class:                     '             #26db51',         
            Token.Name.Constant:                  '             #e6bb00',         
            Token.Name.Decorator:                 '             #26db51',         
            Token.Name.Entity:                    '             #86ff00',         
            Token.Name.Exception:                 '             #b1fb00',         
            Token.Name.Function:                  '             #91bb00',         
            Token.Name.Label:                     '             #26ff31',         
            Token.Name.Namespace:                 '             #26ff31',         
            Token.Name.Other:                     ' ',                            
            Token.Name.Property:                  ' ',                            
            Token.Name.Tag:                       '             #269086',         
            Token.Name.Variable:                  '             #dc9b00',         
            Token.Name.Variable.Class:            ' ',                            
            Token.Name.Variable.Global:           '             #b1fb00',         
            Token.Name.Variable.Instance:         ' ',                            
            Token.Operator:                       '             #79ce24',         
            Token.Operator.Word:                  '             #d1a67c',         
            Token.Other:                          ' ',                            
            Token.Punctuation:                    '             #a6fb51',         
            Token.Text:                           ' ',                            
            Token.Text.Whitespace:                '             #d1ff00'}         


snape_style={Token: '',
            Token.Comment:                        ' italic      #51a6fb',         
            Token.Comment.Hashbang:               '             #5126db',         
            Token.Comment.Multiline:              '             #51a6fb',         
            Token.Comment.Preproc:                ' noitalic    #3126ff',         
            Token.Comment.PreprocFile:            ' ',                            
            Token.Comment.Single:                 ' ',                            
            Token.Comment.Special:                ' ',                            
            Token.Error:                          ' bg:         #7cd1a6',         
            Token.Escape:                         ' ',                            
            Token.Generic:                        ' ',                            
            Token.Generic.Deleted:                '             #00f17b',         
            Token.Generic.Emph:                   ' italic',                      
            Token.Generic.Error:                  '             #00f17b',         
            Token.Generic.Heading:                '             #2479ce',         
            Token.Generic.Inserted:               '             #003cf0',         
            Token.Generic.Output:                 '             #2479ce',         
            Token.Generic.Prompt:                 '             #004ca0',         
            Token.Generic.Strong:                 ' bold',                        
            Token.Generic.Subheading:             '             #004ca0',         
            Token.Generic.Traceback:              '             #862690',         
            Token.Keyword:                        '             #862690 bold',    
            Token.Keyword.Constant:               ' italic      #004ca0',         
            Token.Keyword.Declaration:            ' italic',                      
            Token.Keyword.Pseudo:                 ' ',                            
            Token.Keyword.Reserved:               ' ',                            
            Token.Keyword.Type:                   ' italic',                      
            Token.Literal:                        ' ',                            
            Token.Literal.Date:                   ' ',                            
            Token.Literal.Number:                 '             #004ca0',         
            Token.Literal.Number.Bin:             ' ',                            
            Token.Literal.Number.Float:           ' ',                            
            Token.Literal.Number.Hex:             ' ',                            
            Token.Literal.Number.Integer:         ' ',                            
            Token.Literal.Number.Integer.Long:    ' ',                            
            Token.Literal.Number.Oct:             ' ',                            
            Token.Literal.String:                 '             #00e690',         
            Token.Literal.String.Backtick:        ' ',                            
            Token.Literal.String.Char:            '             #7cd1a6',         
            Token.Literal.String.Doc:             ' italic      #00e6bb',         
            Token.Literal.String.Double:          ' ',                            
            Token.Literal.String.Escape:          '             #0086ff',         
            Token.Literal.String.Heredoc:         ' ',                            
            Token.Literal.String.Interpol:        ' underline',                    
            Token.Literal.String.Other:           '             #7cd1a6',         
            Token.Literal.String.Regex:           '             #7cd1a6',         
            Token.Literal.String.Single:          ' ',                            
            Token.Literal.String.Symbol:          ' ',                            
            Token.Name:                           ' ',                            
            Token.Name.Attribute:                 '             #003cf0',         
            Token.Name.Builtin:                   '             #003cf0',         
            Token.Name.Builtin.Pseudo:            ' italic',                      
            Token.Name.Class:                     '             #5126db',         
            Token.Name.Constant:                  '             #00e6bb',         
            Token.Name.Decorator:                 '             #5126db',         
            Token.Name.Entity:                    '             #0086ff',         
            Token.Name.Exception:                 '             #00b1fb',         
            Token.Name.Function:                  '             #0091bb',         
            Token.Name.Label:                     '             #3126ff',         
            Token.Name.Namespace:                 '             #3126ff',         
            Token.Name.Other:                     ' ',                            
            Token.Name.Property:                  ' ',                            
            Token.Name.Tag:                       '             #862690',         
            Token.Name.Variable:                  '             #00dc9b',         
            Token.Name.Variable.Class:            ' ',                            
            Token.Name.Variable.Global:           '             #00b1fb',         
            Token.Name.Variable.Instance:         ' ',                            
            Token.Operator:                       '             #2479ce',         
            Token.Operator.Word:                  '             #7cd1a6',         
            Token.Other:                          ' ',                            
            Token.Punctuation:                    '             #51a6fb',         
            Token.Text:                           ' ',                            
            Token.Text.Whitespace:                '             #00d1ff'}         


# ryan_style= \
#     {
#         # A rich, colored scheme I made (based on monokai)
#         Comment:"#00ff00",
#         Keyword:'#44ff44',
#         Number:'#378cba',
#         Operator:'',
#         String:'#26b534',
#         Token.Literal.String.Escape :"  #ae81ff",
#         #
#         Name:'',
#         Name.Decorator:'#ff4444',
#         Name.Class:'#ff4444',
#         Name.Function:'#ff4444',
#         Name.Builtin:'#ff4444',
#         #
#         Name.Attribute:'',
#         Name.Constant:'',
#         Name.Entity:'',
#         Name.Exception:'',
#         Name.Label:'',
#         Name.Namespace:'#dcff2d',
#         Name.Tag:'',
#         Name.Variable:'',
#     }


def generate_style(python_style, ui_style):
    """
    Generate Pygments Style class from two dictionaries
    containing style rules.
    """
    assert isinstance(python_style, dict)
    assert isinstance(ui_style, dict)

    styles = {}
    styles.update(DEFAULT_STYLE_EXTENSIONS)
    styles.update(python_style)
    styles.update(ui_style)

    return style_from_dict(styles)


# Code style for Windows consoles. They support only 16 colors,
# so we choose a combination that displays nicely.
win32_code_style = {
    Comment:                   "#00ff00",
    Keyword:                   '#44ff44',
    Number:                    '',
    Operator:                  '',
    String:                    '#ff44ff',

    Name:                      '',
    Name.Decorator:            '#ff4444',
    Name.Class:                '#ff4444',
    Name.Function:             '#ff4444',
    Name.Builtin:              '#ff4444',

    Name.Attribute:            '',
    Name.Constant:             '',
    Name.Entity:               '',
    Name.Exception:            '',
    Name.Label:                '',
    Name.Namespace:            '',
    Name.Tag:                  '',
    Name.Variable:             '',
}
default_ui_style = {
    Token.LineNumber:'#aa6666 bg:#002222',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #008800',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#ff0000',
    Token.Out.Number:                             '#ff0000',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#bbbbbb',

    # Search toolbar.
    Token.Toolbar.Search:                         '#22aaaa noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#22aaaa noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#22aaaa noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#44bbbb #000000',
    Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',
    Token.Toolbar.Signature.Operator:             '#000000 bold',

    Token.Docstring:                              '#888888',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',
    Token.Toolbar.Status.Key:                     'bg:#000000 #888888',
    Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable: 'bg:#662266 #aaaaaa',
    Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#888888',

    # The options sidebar.
    Token.Sidebar:                                'bg:#bbbbbb #000000',
    Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',
    Token.Sidebar.Label:                          'bg:#bbbbbb #222222',
    Token.Sidebar.Status:                         'bg:#dddddd #000011',
    Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',
    Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',

    Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',
    Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',
    Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',
    Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#008800  #000000',
    Token.History.Line.Current:                  'bg:#ffffff #000000',
    Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',
    Token.History.ExistingInput:                  '#888888',

    # Help Window.
    Token.Window.Border:                          '#0000bb',
    Token.Window.Title:                           'bg:#bbbbbb #000000',
    Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#ffff88 #444444',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#884444 #ffffff',
}

# Some changes to get a bit more contrast on Windows consoles.
# (They only support 16 colors.)
if is_windows() and not is_conemu_ansi():
    default_ui_style.update({
        Token.Sidebar.Title:                          'bg:#00ff00 #ffffff',
        Token.ExitConfirmation:                       'bg:#ff4444 #ffffff',
        Token.Toolbar.Validation:                     'bg:#ff4444 #ffffff',

        Token.Menu.Completions.Completion:            'bg:#ffffff #000000',
        Token.Menu.Completions.Completion.Current:    'bg:#aaaaaa #000000',
    })


blue_ui_style = {}
blue_ui_style.update(default_ui_style)
blue_ui_style.update({
        # Line numbers.
        Token.LineNumber:                             '#aa6666 bg:#222222',

        # Highlighting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#4444aa',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        # Highlighting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#6666aa',

        # Completer toolbar.
        Token.Toolbar.Completions:                    'bg:#44bbbb #000000',
        Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',
        Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',
        Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',

        # Completer menu.
        Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',
        Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',
        Token.Menu.Completions.Meta:                  'bg:#449999 #000000',
        Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',
        Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        Token.Menu.Completions.ProgressButton:        'bg:#000000',
})


# HOW I MADE THE INVERSION THEME:
#THIS CODE AUTOMATICALLY MODIFIES COLORS IN THESE THEMES WHICH LETS ME MAKE NEW THEMES
# code="""{Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #008800',Token.In.Number:                              '',Token.Out:                                    '#ff0000',Token.Out.Number:                             '#ff0000',Token.Separator:                              '#bbbbbb',Token.Toolbar.Search:                         '#22aaaa noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#22aaaa noinherit',Token.Toolbar.Arg:                            '#22aaaa noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#44bbbb #000000',Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',Token.Toolbar.Signature.Operator:             '#000000 bold',Token.Docstring:                              '#888888',Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',Token.Toolbar.Status.Key:                     'bg:#000000 #888888',Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',Token.Aborted:                                '#888888',Token.Sidebar:                                'bg:#bbbbbb #000000',Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',Token.Sidebar.Label:                          'bg:#bbbbbb #222222',Token.Sidebar.Status:                         'bg:#dddddd #000011',Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#008800  #000000',Token.History.Line.Current:                  'bg:#ffffff #000000',Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',Token.History.ExistingInput:                  '#888888',Token.Window.Border:                          '#0000bb',Token.Window.Title:                           'bg:#bbbbbb #000000',Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',Token.AcceptMessage:                          'bg:#ffff88 #444444',Token.ExitConfirmation:                       'bg:#884444 #ffffff',}"""
# def changecolors(colors):
#     return [np.clip((np.roll([x for x in c],1)*2+np.asarray([0,128,255]))//1.5-100,0,255).astype(int) for c in colors]
# def codewithcolors(colors,code=code):
#     x=keys_and_values_to_dict(tocols(allcols(code)),tocols(colors))
#     print(x)
#     return search_replace_simul(code,x)
# def tocols(cols):
#     return [''.join([hex(x)[2:].rjust(2,'0') for x in y]) for y in cols]
# def allcols(code):
#     import re
#     cols=re.findall('#'+r'[\dA-Fa-f]'*6,code)#Colors like 55aaff or 12abfg
#     cols=[x[1:] for x in cols]
#     cols=set(cols)
#     return [[eval('0x'+''.join(x)) for x in split_into_sublists(w,2)] for w in cols]
# colors=allcols(code)
# ans=codewithcolors(changecolors(colors),code)

inverted_3 = {}
inverted_3.update(default_ui_style)

inverted_3 = {}
inverted_3.update(default_ui_style)
inverted_3.update({
    # Status toolbar.

    # Token.Toolbar.Status:                         'bg:#dddddd #555555',
    # Token.Toolbar.Status.BatteryPluggedIn:        'bg:#dddddd #dd55dd',
    # Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#dddddd #55dddd',
    # Token.Toolbar.Status.Title:                   'underline',
    # Token.Toolbar.Status.InputMode:               'bg:#dddddd #000055',
    # Token.Toolbar.Status.Key:                     'bg:#ffffff #777777',
    # Token.Toolbar.Status.PasteModeOn:             'bg:#55bbbb #000000',
    # Token.Toolbar.Status.PseudoTerminalCurrentVariable:
    #     'bg:#99dd99 #555555',# RYAN BURGERT STUFF
    # Token.Toolbar.Status.PythonVersion:           'bg:#dddddd #000000 bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#777777',

    # The options sidebar.
    Token.Sidebar:                                'bg:#444444 #ffffff',
    Token.Sidebar.Title:                          'bg:#997700 #000000 bold',
    Token.Sidebar.Label:                          'bg:#444444 #dddddd',
    Token.Sidebar.Status:                         'bg:#222222 #ffffee',
    Token.Sidebar.Selected.Label:                 'bg:#dddddd #111111',
    Token.Sidebar.Selected.Status:                'bg:#bbbbbb #000000 bold',

    Token.Sidebar.Separator:                       'bg:#444444 #000000 underline',
    Token.Sidebar.Key:                            'bg:#442244 #ffffff bold',
    Token.Sidebar.Key.Description:                'bg:#444444 #ffffff',
    Token.Sidebar.HelpText:                       'bg:#111100 #ffffee',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#ff77ff  #ffffff',
    Token.History.Line.Current:                  'bg:#000000 #ffffff',
    Token.History.Line.Selected.Current:         'bg:#770077 #ffffff',
    Token.History.ExistingInput:                  '#777777',

    # Help Window.
    Token.Window.Border:                          '#ffff44',
    Token.Window.Title:                           'bg:#444444 #ffffff',
    Token.Window.TIItleV2:                         'bg:#997744 #ffffff bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#000077 #bbbbbb',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#77bbbb #000000',
})

inverted_3.update({
        # Line numbers.
        Token.LineNumber:                             '#aa6666 bg:#222222',

        # Highlighting of search matches in document.
        Token.SearchMatch:                            '#ffffff bg:#4444aa',
        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',

        # Highlighting of select text in document.
        Token.SelectedText:                           '#ffffff bg:#6666aa',

        # # Completer toolbar.
        # Token.Toolbar.Completions:                    'bg:#44bbbb #000000',
        # Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',
        # Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',
        # Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',

        # # Completer menu.
        # Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',
        # Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',
        # Token.Menu.Completions.Meta:                  'bg:#449999 #000000',
        # Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',
        # Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',
        # Token.Menu.Completions.ProgressButton:        'bg:#000000',



                Token.Toolbar.Completions:            'bg:#000046 #bf954c',
        Token.Toolbar.Completions.Arrow:              'bg:#000046 #bf954c bold',
        Token.Toolbar.Completions.Completion:         'bg:#000046 #bf954c',
        Token.Toolbar.Completions.Completion.Current: 'bg:#f0ffff #6a5100',



        # Completer menu.
        Token.Menu.Completions.Completion:            'bg:#202046 #ff954c',
        Token.Menu.Completions.Completion.Current:    'bg:#ff954c #202046',
        Token.Menu.Completions.Meta:                  'bg:#000046 #ff684c',
        Token.Menu.Completions.Meta.Current:          'bg:#000046 #ff7e00',
        Token.Menu.Completions.ProgressBar:           'bg:#ff7ed4           ',
        Token.Menu.Completions.ProgressButton:        'bg:#460000           ',
})






color_1={    Token.LineNumber:'#d47623 bg:#397300',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #7dfb00',    Token.In.Number:                              '',    Token.Out:                                    '#ff0039',    Token.Out.Number:                             '#ff0039',    Token.Separator:                              '#ffdf94',    Token.Toolbar.Search:                         '#2eff1e noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#2eff1e noinherit',    Token.Toolbar.Arg:                            '#2eff1e noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#5cff4c #234600',    Token.Toolbar.Signature.CurrentName:          'bg:#2cfb00 #fff7f0 bold',    Token.Toolbar.Signature.Operator:             '#234600 bold',    Token.Docstring:                              '#fbfb51',    Token.Toolbar.Validation:                     'bg:#4c2000 #ffe97e',    Token.Toolbar.Status:                         'bg:#577300 #ffe97e',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#577300 #9dff00',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#577300 #d40900',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#577300 #ffbe7e',    Token.Toolbar.Status.Key:                     'bg:#234600 #fbfb51',    Token.Toolbar.Status.PasteModeOn:             'bg:#d43500 #fff7f0',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#794824 #ffe97e',    Token.Toolbar.Status.PythonVersion:           'bg:#577300 #fff7f0 bold',    Token.Aborted:                                '#fbfb51',    Token.Sidebar:                                'bg:#ffdf94 #234600',    Token.Sidebar.Title:                          'bg:#79fbaf #444488 bold',    Token.Sidebar.Label:                          'bg:#ffdf94 #577300',    Token.Sidebar.Status:                         'bg:#ffe0c2 #234600',    Token.Sidebar.Selected.Label:                 'bg:#577300 #ffecd9',    Token.Sidebar.Selected.Status:                'bg:#9ba000 #fff7f0 bold',    Token.Sidebar.Separator:                       'bg:#ffdf94 #fff7f0 underline',    Token.Sidebar.Key:                            'bg:#ffdf94 #234600 bold',    Token.Sidebar.Key.Description:                'bg:#ffdf94 #234600',    Token.Sidebar.HelpText:                       'bg:#fff7f0 #234600',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#7dfb00  #234600',    Token.History.Line.Current:                  'bg:#fff7f0 #234600',    Token.History.Line.Selected.Current:         'bg:#fdff51 #234600',    Token.History.ExistingInput:                  '#fbfb51',    Token.Window.Border:                          '#009095',    Token.Window.Title:                           'bg:#ffdf94 #234600',    Token.Window.TIItleV2:                         'bg:#9dfb79 #234600 bold',    Token.AcceptMessage:                          'bg:#ffa851 #9ba000',    Token.ExitConfirmation:                       'bg:#a64c00 #fff7f0',    Token.LineNumber:                             '#d47623 bg:#577300',        Token.SearchMatch:                            '#fff7f0 bg:#4ca053',        Token.SearchMatch.Current:                    '#fff7f0 bg:#cbff00',        Token.SelectedText:                           '#fff7f0 bg:#9ece78',        Token.Toolbar.Completions:                    'bg:#5cff4c #234600',        Token.Toolbar.Completions.Arrow:              'bg:#5cff4c #234600 bold',        Token.Toolbar.Completions.Completion:         'bg:#5cff4c #234600',        Token.Toolbar.Completions.Completion.Current: 'bg:#2cfb00 #fff7f0',        Token.Menu.Completions.Completion:            'bg:#5cff4c #234600',        Token.Menu.Completions.Completion.Current:    'bg:#2cfb00 #fff7f0',        Token.Menu.Completions.Meta:                  'bg:#89ff4c #234600',        Token.Menu.Completions.Meta.Current:          'bg:#01ff00 #234600',        Token.Menu.Completions.ProgressBar:           'bg:#ffe97e',        Token.Menu.Completions.ProgressButton:        'bg:#234600',}
color_2={    Token.LineNumber:'#1a1ea2 bg:#410040',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #c900c8',    Token.In.Number:                              '',    Token.Out:                                    '#0094cd',    Token.Out.Number:                             '#0094cd',    Token.Separator:                              '#8876cd',    Token.Toolbar.Search:                         '#cd187f noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#cd187f noinherit',    Token.Toolbar.Arg:                            '#cd187f noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#cd3d91 #140014',    Token.Toolbar.Signature.CurrentName:          'bg:#c90087 #c0c1cd bold',    Token.Toolbar.Signature.Operator:             '#140014 bold',    Token.Docstring:                              '#8440c9',    Token.Toolbar.Validation:                     'bg:#00021a #8765cd',    Token.Toolbar.Status:                         'bg:#300041 #8765cd',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#300041 #b500cd',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#300041 #004aa2',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#300041 #6565cd',    Token.Toolbar.Status.Key:                     'bg:#140014 #8440c9',    Token.Toolbar.Status.PasteModeOn:             'bg:#0028a2 #c0c1cd',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#151847 #8765cd',    Token.Toolbar.Status.PythonVersion:           'bg:#300041 #c0c1cd bold',    Token.Aborted:                                '#8440c9',    Token.Sidebar:                                'bg:#8876cd #140014',    Token.Sidebar.Title:                          'bg:#c96069 #c0c1cd bold',    Token.Sidebar.Label:                          'bg:#8876cd #300041',    Token.Sidebar.Status:                         'bg:#9b9ccd #140014',    Token.Sidebar.Selected.Label:                 'bg:#300041 #aeaecd',    Token.Sidebar.Selected.Status:                'bg:#3a006e #c0c1cd bold',    Token.Sidebar.Separator:                       'bg:#8876cd #c0c1cd underline',    Token.Sidebar.Key:                            'bg:#8876cd #140014 bold',    Token.Sidebar.Key.Description:                'bg:#8876cd #140014',    Token.Sidebar.HelpText:                       'bg:#c0c1cd #140014',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#c900c8  #140014',    Token.History.Line.Current:                  'bg:#c0c1cd #140014',    Token.History.Line.Selected.Current:         'bg:#8841cd #140014',    Token.History.ExistingInput:                  '#8440c9',    Token.Window.Border:                          '#633400',    Token.Window.Title:                           'bg:#8876cd #140014',    Token.Window.TIItleV2:                         'bg:#c960b1 #140014 bold',    Token.AcceptMessage:                          'bg:#4141cd #3a006e',    Token.ExitConfirmation:                       'bg:#000474 #c0c1cd',    Token.LineNumber:                             '#1a1ea2 bg:#300041',        Token.SearchMatch:                            '#c0c1cd bg:#6e344c',        Token.SearchMatch.Current:                    '#c0c1cd bg:#9000cd',        Token.SelectedText:                           '#c0c1cd bg:#9c5a98',        Token.Toolbar.Completions:                    'bg:#cd3d91 #140014',        Token.Toolbar.Completions.Arrow:              'bg:#cd3d91 #140014 bold',        Token.Toolbar.Completions.Completion:         'bg:#cd3d91 #140014',        Token.Toolbar.Completions.Completion.Current: 'bg:#c90087 #c0c1cd',        Token.Menu.Completions.Completion:            'bg:#cd3d91 #140014',        Token.Menu.Completions.Completion.Current:    'bg:#c90087 #c0c1cd',        Token.Menu.Completions.Meta:                  'bg:#cd3db6 #140014',        Token.Menu.Completions.Meta.Current:          'bg:#cd0067 #140014',        Token.Menu.Completions.ProgressBar:           'bg:#8765cd',        Token.Menu.Completions.ProgressButton:        'bg:#140014',}
color_3={    Token.LineNumber:'#5ea28b bg:#202941',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #6482c9',    Token.In.Number:                              '',    Token.Out:                                    '#68cd66',    Token.Out.Number:                             '#68cd66',    Token.Separator:                              '#a1cdc8',    Token.Toolbar.Search:                         '#7e72cd noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#7e72cd noinherit',    Token.Toolbar.Arg:                            '#7e72cd noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#8d85cd #0a0c14',    Token.Toolbar.Signature.CurrentName:          'bg:#6764c9 #c6cdca bold',    Token.Toolbar.Signature.Operator:             '#0a0c14 bold',    Token.Docstring:                              '#84bbc9',    Token.Toolbar.Validation:                     'bg:#0d1a15 #99cbcd',    Token.Toolbar.Status:                         'bg:#203241 #99cbcd',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#203241 #6691cd',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#203241 #51a264',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#203241 #99cdbd',    Token.Toolbar.Status.Key:                     'bg:#0a0c14 #84bbc9',    Token.Toolbar.Status.PasteModeOn:             'bg:#51a275 #c6cdca',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#2e473e #99cbcd',    Token.Toolbar.Status.PythonVersion:           'bg:#203241 #c6cdca bold',    Token.Aborted:                                '#84bbc9',    Token.Sidebar:                                'bg:#a1cdc8 #0a0c14',    Token.Sidebar.Title:                          'bg:#b494c9 #c6cdca bold',    Token.Sidebar.Label:                          'bg:#a1cdc8 #203241',    Token.Sidebar.Status:                         'bg:#b4cdc5 #0a0c14',    Token.Sidebar.Selected.Label:                 'bg:#203241 #bdcdc8',    Token.Sidebar.Selected.Status:                'bg:#37616e #c6cdca bold',    Token.Sidebar.Separator:                       'bg:#a1cdc8 #c6cdca underline',    Token.Sidebar.Key:                            'bg:#a1cdc8 #0a0c14 bold',    Token.Sidebar.Key.Description:                'bg:#a1cdc8 #0a0c14',    Token.Sidebar.HelpText:                       'bg:#c6cdca #0a0c14',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#6482c9  #0a0c14',    Token.History.Line.Current:                  'bg:#c6cdca #0a0c14',    Token.History.Line.Selected.Current:         'bg:#86becd #0a0c14',    Token.History.ExistingInput:                  '#84bbc9',    Token.Window.Border:                          '#633157',    Token.Window.Title:                           'bg:#a1cdc8 #0a0c14',    Token.Window.TIItleV2:                         'bg:#9498c9 #0a0c14 bold',    Token.AcceptMessage:                          'bg:#86cdb8 #37616e',    Token.ExitConfirmation:                       'bg:#3a7460 #c6cdca',    Token.LineNumber:                             '#5ea28b bg:#203241',        Token.SearchMatch:                            '#c6cdca bg:#59516e',        Token.SearchMatch.Current:                    '#c6cdca bg:#66a3cd',        Token.SelectedText:                           '#c6cdca bg:#7b829c',        Token.Toolbar.Completions:                    'bg:#8d85cd #0a0c14',        Token.Toolbar.Completions.Arrow:              'bg:#8d85cd #0a0c14 bold',        Token.Toolbar.Completions.Completion:         'bg:#8d85cd #0a0c14',        Token.Toolbar.Completions.Completion.Current: 'bg:#6764c9 #c6cdca',        Token.Menu.Completions.Completion:            'bg:#8d85cd #0a0c14',        Token.Menu.Completions.Completion.Current:    'bg:#6764c9 #c6cdca',        Token.Menu.Completions.Meta:                  'bg:#858fcd #0a0c14',        Token.Menu.Completions.Meta.Current:          'bg:#7a66cd #0a0c14',        Token.Menu.Completions.ProgressBar:           'bg:#99cbcd',        Token.Menu.Completions.ProgressButton:        'bg:#0a0c14',}

pupper= {    Token.LineNumber:'#23d452 bg:#005073',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #00affb',    Token.In.Number:                              '',    Token.Out:                                    '#6cff00',    Token.Out.Number:                             '#6cff00',    Token.Separator:                              '#94ffc9',    Token.Toolbar.Search:                         '#1e5bff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#1e5bff noinherit',    Token.Toolbar.Arg:                            '#1e5bff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#4c80ff #003046',    Token.Toolbar.Signature.CurrentName:          'bg:#005efb #f0fff4 bold',    Token.Toolbar.Signature.Operator:             '#003046 bold',    Token.Docstring:                              '#51fbd8',    Token.Toolbar.Validation:                     'bg:#004c10 #7effcf',    Token.Toolbar.Status:                         'bg:#006e73 #7effcf',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#006e73 #00d0ff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#006e73 #21d400',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#006e73 #7effa4',    Token.Toolbar.Status.Key:                     'bg:#003046 #51fbd8',    Token.Toolbar.Status.PasteModeOn:             'bg:#00d40b #f0fff4',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247937 #7effcf',    Token.Toolbar.Status.PythonVersion:           'bg:#006e73 #f0fff4 bold',    Token.Aborted:                                '#51fbd8',    Token.Sidebar:                                'bg:#94ffc9 #003046',    Token.Sidebar.Title:                          'bg:#9479fb #f0fff4 bold',    Token.Sidebar.Label:                          'bg:#94ffc9 #006e73',    Token.Sidebar.Status:                         'bg:#c2ffd4 #003046',    Token.Sidebar.Selected.Label:                 'bg:#006e73 #d9ffe4',    Token.Sidebar.Selected.Status:                'bg:#00a084 #f0fff4 bold',    Token.Sidebar.Separator:                       'bg:#94ffc9 #f0fff4 underline',    Token.Sidebar.Key:                            'bg:#94ffc9 #003046 bold',    Token.Sidebar.Key.Description:                'bg:#94ffc9 #003046',    Token.Sidebar.HelpText:                       'bg:#f0fff4 #003046',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#00affb  #003046',    Token.History.Line.Current:                  'bg:#f0fff4 #003046',    Token.History.Line.Selected.Current:         'bg:#51ffde #003046',    Token.History.ExistingInput:                  '#51fbd8',    Token.Window.Border:                          '#7b0095',    Token.Window.Title:                           'bg:#94ffc9 #003046',    Token.Window.TIItleV2:                         'bg:#79b8fb #003046 bold',    Token.AcceptMessage:                          'bg:#51ff85 #00a084',    Token.ExitConfirmation:                       'bg:#00a62b #f0fff4',    Token.LineNumber:                             '#23d452 bg:#006e73',        Token.SearchMatch:                            '#f0fff4 bg:#4c54a0',        Token.SearchMatch.Current:                    '#f0fff4 bg:#00feff',        Token.SelectedText:                           '#f0fff4 bg:#78afce',        Token.Toolbar.Completions:                    'bg:#4c80ff #003046',        Token.Toolbar.Completions.Arrow:              'bg:#4c80ff #003046 bold',        Token.Toolbar.Completions.Completion:         'bg:#4c80ff #003046',        Token.Toolbar.Completions.Completion.Current: 'bg:#005efb #f0fff4',        Token.Menu.Completions.Completion:            'bg:#4c80ff #003046',        Token.Menu.Completions.Completion.Current:    'bg:#005efb #f0fff4',        Token.Menu.Completions.Meta:                  'bg:#4cadff #003046',        Token.Menu.Completions.Meta.Current:          'bg:#0034ff #003046',        Token.Menu.Completions.ProgressBar:           'bg:#7effcf',        Token.Menu.Completions.ProgressButton:        'bg:#003046',}
clara=  {    Token.LineNumber:'#7bced4 bg:#3f3973',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #8a7dfb',    Token.In.Number:                              '',    Token.Out:                                    '#7fffaf',    Token.Out.Number:                             '#7fffaf',    Token.Separator:                              '#c9efff',    Token.Toolbar.Search:                         '#ca8eff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#ca8eff noinherit',    Token.Toolbar.Arg:                            '#ca8eff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#d3a5ff #262346',    Token.Toolbar.Signature.CurrentName:          'bg:#b27dfb #f7feff bold',    Token.Toolbar.Signature.Operator:             '#262346 bold',    Token.Docstring:                              '#a6c8fb',    Token.Toolbar.Validation:                     'bg:#264b4c #bee3ff',    Token.Toolbar.Status:                         'bg:#394273 #bee3ff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#394273 #7f81ff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#394273 #6ad4ae',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#394273 #bef8ff',    Token.Toolbar.Status.Key:                     'bg:#262346 #a6c8fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#6ad4c4 #f7feff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#4e7879 #bee3ff',    Token.Toolbar.Status.PythonVersion:           'bg:#394273 #f7feff bold',    Token.Aborted:                                '#a6c8fb',    Token.Sidebar:                                'bg:#c9efff #262346',    Token.Sidebar.Title:                          'bg:#fbbafa #f7feff bold',    Token.Sidebar.Label:                          'bg:#c9efff #394273',    Token.Sidebar.Status:                         'bg:#e0fcff #262346',    Token.Sidebar.Selected.Label:                 'bg:#394273 #ecfdff',    Token.Sidebar.Selected.Status:                'bg:#506da0 #f7feff bold',    Token.Sidebar.Separator:                       'bg:#c9efff #f7feff underline',    Token.Sidebar.Key:                            'bg:#c9efff #262346 bold',    Token.Sidebar.Key.Description:                'bg:#c9efff #262346',    Token.Sidebar.HelpText:                       'bg:#f7feff #262346',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#8a7dfb  #262346',    Token.History.Line.Current:                  'bg:#f7feff #262346',    Token.History.Line.Selected.Current:         'bg:#a8c9ff #262346',    Token.History.ExistingInput:                  '#a6c8fb',    Token.Window.Border:                          '#954a66',    Token.Window.Title:                           'bg:#c9efff #262346',    Token.Window.TIItleV2:                         'bg:#cebafb #262346 bold',    Token.AcceptMessage:                          'bg:#a8f6ff #506da0',    Token.ExitConfirmation:                       'bg:#53a1a6 #f7feff',    Token.LineNumber:                             '#7bced4 bg:#394273',        Token.SearchMatch:                            '#f7feff bg:#9376a0',        Token.SearchMatch.Current:                    '#f7feff bg:#7f98ff',        Token.SelectedText:                           '#f7feff bg:#a9a3ce',        Token.Toolbar.Completions:                    'bg:#d3a5ff #262346',        Token.Toolbar.Completions.Arrow:              'bg:#d3a5ff #262346 bold',        Token.Toolbar.Completions.Completion:         'bg:#d3a5ff #262346',        Token.Toolbar.Completions.Completion.Current: 'bg:#b27dfb #f7feff',        Token.Menu.Completions.Completion:            'bg:#d3a5ff #262346',        Token.Menu.Completions.Completion.Current:    'bg:#b27dfb #f7feff',        Token.Menu.Completions.Meta:                  'bg:#bca5ff #262346',        Token.Menu.Completions.Meta.Current:          'bg:#cb7fff #262346',        Token.Menu.Completions.ProgressBar:           'bg:#bee3ff',        Token.Menu.Completions.ProgressButton:        'bg:#262346',}
emma=   {    Token.LineNumber:'#7b86d4 bg:#6d3973',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #ee7dfb',    Token.In.Number:                              '',    Token.Out:                                    '#7fe8ff',    Token.Out.Number:                             '#7fe8ff',    Token.Separator:                              '#cec9ff',    Token.Toolbar.Search:                         '#ff8ed9 noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#ff8ed9 noinherit',    Token.Toolbar.Arg:                            '#ff8ed9 noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#ffa4e3 #412346',    Token.Toolbar.Signature.CurrentName:          'bg:#fb7ddf #f7f7ff bold',    Token.Toolbar.Signature.Operator:             '#412346 bold',    Token.Docstring:                              '#c8a6fb',    Token.Toolbar.Validation:                     'bg:#262c4c #cdbeff',    Token.Toolbar.Status:                         'bg:#5e3973 #cdbeff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#5e3973 #e37fff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#5e3973 #6aa5d4',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#5e3973 #bec4ff',    Token.Toolbar.Status.Key:                     'bg:#412346 #c8a6fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#6a8fd4 #f7f7ff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#4e5579 #cdbeff',    Token.Toolbar.Status.PythonVersion:           'bg:#5e3973 #f7f7ff bold',    Token.Aborted:                                '#c8a6fb',    Token.Sidebar:                                'bg:#cec9ff #412346',    Token.Sidebar.Title:                          'bg:#fbbac6 #f7f7ff bold',    Token.Sidebar.Label:                          'bg:#cec9ff #5e3973',    Token.Sidebar.Status:                         'bg:#e0e3ff #412346',    Token.Sidebar.Selected.Label:                 'bg:#5e3973 #ecedff',    Token.Sidebar.Selected.Status:                'bg:#7350a0 #f7f7ff bold',    Token.Sidebar.Separator:                       'bg:#cec9ff #f7f7ff underline',    Token.Sidebar.Key:                            'bg:#cec9ff #412346 bold',    Token.Sidebar.Key.Description:                'bg:#cec9ff #412346',    Token.Sidebar.HelpText:                       'bg:#f7f7ff #412346',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#ee7dfb  #412346',    Token.History.Line.Current:                  'bg:#f7f7ff #412346',    Token.History.Line.Selected.Current:         'bg:#cca8ff #412346',    Token.History.ExistingInput:                  '#c8a6fb',    Token.Window.Border:                          '#956a49',    Token.Window.Title:                           'bg:#cec9ff #412346',    Token.Window.TIItleV2:                         'bg:#fbbaf4 #412346 bold',    Token.AcceptMessage:                          'bg:#a8b0ff #7350a0',    Token.ExitConfirmation:                       'bg:#535ea6 #f7f7ff',    Token.LineNumber:                             '#7b86d4 bg:#5e3973',        Token.SearchMatch:                            '#f7f7ff bg:#a0768b',        Token.SearchMatch.Current:                    '#f7f7ff bg:#cc7fff',        Token.SelectedText:                           '#f7f7ff bg:#cba3ce',        Token.Toolbar.Completions:                    'bg:#ffa4e3 #412346',        Token.Toolbar.Completions.Arrow:              'bg:#ffa4e3 #412346 bold',        Token.Toolbar.Completions.Completion:         'bg:#ffa4e3 #412346',        Token.Toolbar.Completions.Completion.Current: 'bg:#fb7ddf #f7f7ff',        Token.Menu.Completions.Completion:            'bg:#ffa4e3 #412346',        Token.Menu.Completions.Completion.Current:    'bg:#fb7ddf #f7f7ff',        Token.Menu.Completions.Meta:                  'bg:#ffa4fa #412346',        Token.Menu.Completions.Meta.Current:          'bg:#ff7fcc #412346',        Token.Menu.Completions.ProgressBar:           'bg:#cdbeff',        Token.Menu.Completions.ProgressButton:        'bg:#412346',}

base=   {    Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #008800',    Token.In.Number:                              '',    Token.Out:                                    '#ff0000',    Token.Out.Number:                             '#ff0000',    Token.Separator:                              '#bbbbbb',    Token.Toolbar.Search:                         '#22aaaa noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#22aaaa noinherit',    Token.Toolbar.Arg:                            '#22aaaa noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#44bbbb #000000',    Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',    Token.Toolbar.Signature.Operator:             '#000000 bold',    Token.Docstring:                              '#888888',    Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',    Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',    Token.Toolbar.Status.Key:                     'bg:#000000 #888888',    Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',    Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',    Token.Aborted:                                '#888888',    Token.Sidebar:                                'bg:#bbbbbb #000000',    Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',    Token.Sidebar.Label:                          'bg:#bbbbbb #222222',    Token.Sidebar.Status:                         'bg:#dddddd #000011',    Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',    Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',    Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',    Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',    Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',    Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#008800  #000000',    Token.History.Line.Current:                  'bg:#ffffff #000000',    Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',    Token.History.ExistingInput:                  '#888888',    Token.Window.Border:                          '#0000bb',    Token.Window.Title:                           'bg:#bbbbbb #000000',    Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',    Token.AcceptMessage:                          'bg:#ffff88 #444444',    Token.ExitConfirmation:                       'bg:#884444 #ffffff',    Token.LineNumber:                             '#aa6666 bg:#222222',        Token.SearchMatch:                            '#ffffff bg:#4444aa',        Token.SearchMatch.Current:                    '#ffffff bg:#44aa44',        Token.SelectedText:                           '#ffffff bg:#6666aa',        Token.Toolbar.Completions:                    'bg:#44bbbb #000000',        Token.Toolbar.Completions.Arrow:              'bg:#44bbbb #000000 bold',        Token.Toolbar.Completions.Completion:         'bg:#44bbbb #000000',        Token.Toolbar.Completions.Completion.Current: 'bg:#008888 #ffffff',        Token.Menu.Completions.Completion:            'bg:#44bbbb #000000',        Token.Menu.Completions.Completion.Current:    'bg:#008888 #ffffff',        Token.Menu.Completions.Meta:                  'bg:#449999 #000000',        Token.Menu.Completions.Meta.Current:          'bg:#00aaaa #000000',        Token.Menu.Completions.ProgressBar:           'bg:#aaaaaa',        Token.Menu.Completions.ProgressButton:        'bg:#000000',}

inverted_1= {Token.LineNumber:'#aa6666 bg:#002222',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #008800',Token.In.Number:                              '',Token.Out:                                    '#ff0000',Token.Out.Number:                             '#ff0000',Token.Separator:                              '#bbbbbb',Token.Toolbar.Search:                         '#22aaaa noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#22aaaa noinherit',Token.Toolbar.Arg:                            '#22aaaa noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#44bbbb #000000',Token.Toolbar.Signature.CurrentName:          'bg:#008888 #ffffff bold',Token.Toolbar.Signature.Operator:             '#000000 bold',Token.Docstring:                              '#888888',Token.Toolbar.Validation:                     'bg:#440000 #aaaaaa',Token.Toolbar.Status:                         'bg:#222222 #aaaaaa',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#222222 #22aa22',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#222222 #aa2222',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#222222 #ffffaa',Token.Toolbar.Status.Key:                     'bg:#000000 #888888',Token.Toolbar.Status.PasteModeOn:             'bg:#aa4444 #ffffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#662266 #aaaaaa',Token.Toolbar.Status.PythonVersion:           'bg:#222222 #ffffff bold',Token.Aborted:                                '#888888',Token.Sidebar:                                'bg:#bbbbbb #000000',Token.Sidebar.Title:                          'bg:#6688ff #ffffff bold',Token.Sidebar.Label:                          'bg:#bbbbbb #222222',Token.Sidebar.Status:                         'bg:#dddddd #000011',Token.Sidebar.Selected.Label:                 'bg:#222222 #eeeeee',Token.Sidebar.Selected.Status:                'bg:#444444 #ffffff bold',Token.Sidebar.Separator:                       'bg:#bbbbbb #ffffff underline',Token.Sidebar.Key:                            'bg:#bbddbb #000000 bold',Token.Sidebar.Key.Description:                'bg:#bbbbbb #000000',Token.Sidebar.HelpText:                       'bg:#eeeeff #000011',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#008800  #000000',Token.History.Line.Current:                  'bg:#ffffff #000000',Token.History.Line.Selected.Current:         'bg:#88ff88 #000000',Token.History.ExistingInput:                  '#888888',Token.Window.Border:                          '#0000bb',Token.Window.Title:                           'bg:#bbbbbb #000000',Token.Window.TIItleV2:                         'bg:#6688bb #000000 bold',Token.AcceptMessage:                          'bg:#ffff88 #444444',Token.ExitConfirmation:                       'bg:#884444 #ffffff',}
inverted_2 ={Token.LineNumber:'#999955 bg:#ddddff',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #77ffff',Token.In.Number:                              '',Token.Out:                                    '#ffff00',Token.Out.Number:                             '#ffff00',Token.Separator:                              '#444444',Token.Toolbar.Search:                         '#5555dd noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#5555dd noinherit',Token.Toolbar.Arg:                            '#5555dd noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#4444bb #ffffff',Token.Toolbar.Signature.CurrentName:          'bg:#7777ff #000000 bold',Token.Toolbar.Signature.Operator:             '#ffffff bold',Token.Docstring:                              '#777777',Token.Toolbar.Validation:                     'bg:#ffffbb #555555',Token.Toolbar.Status:                         'bg:#dddddd #555555',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#dddddd #55dddd',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#dddddd #dddd55',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#dddddd #005500',Token.Toolbar.Status.Key:                     'bg:#ffffff #777777',Token.Toolbar.Status.PasteModeOn:             'bg:#bbbb55 #000000',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#dd9999 #555555',Token.Toolbar.Status.PythonVersion:           'bg:#dddddd #000000 bold',Token.Aborted:                                '#777777',Token.Sidebar:                                'bg:#444444 #ffffff',Token.Sidebar.Title:                          'bg:#770099 #ffffff bold',Token.Sidebar.Label:                          'bg:#444444 #dddddd',Token.Sidebar.Status:                         'bg:#222222 #ffeeff',Token.Sidebar.Selected.Label:                 'bg:#dddddd #111111',Token.Sidebar.Selected.Status:                'bg:#bbbbbb #000000 bold',Token.Sidebar.Separator:                       'bg:#444444 #000000 underline',Token.Sidebar.Key:                            'bg:#224444 #ffffff bold',Token.Sidebar.Key.Description:                'bg:#444444 #ffffff',Token.Sidebar.HelpText:                       'bg:#110011 #ffeeff',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#77ffff  #ffffff',Token.History.Line.Current:                  'bg:#000000 #ffffff',Token.History.Line.Selected.Current:         'bg:#007777 #ffffff',Token.History.ExistingInput:                  '#777777',Token.Window.Border:                          '#ff44ff',Token.Window.Title:                           'bg:#444444 #ffffff',Token.Window.TIItleV2:                         'bg:#774499 #ffffff bold',Token.AcceptMessage:                          'bg:#007700 #bbbbbb',Token.ExitConfirmation:                       'bg:#bbbb77 #000000',}

cyan = {Token.LineNumber:'#6663bb bg:#93d4e8',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #aad4a4',Token.In.Number:                              '',Token.Out:                                    '#aa2aff',Token.Out.Number:                             '#aa2aff',Token.Separator:                              '#2d5882',Token.Toolbar.Search:                         '#38be8d noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#38be8d noinherit',Token.Toolbar.Arg:                            '#38be8d noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#2da782 #aad4ff',Token.Toolbar.Signature.CurrentName:          'bg:#4fd4a4 #002a55 bold',Token.Toolbar.Signature.Operator:             '#aad4ff bold',Token.Docstring:                              '#4f7aa4',Token.Toolbar.Validation:                     'bg:#aaa7ff #38638d',Token.Toolbar.Status:                         'bg:#93bee8 #38638d',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#93bee8 #93be8d',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#93bee8 #9363e8',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#93bee8 #382a55',Token.Toolbar.Status.Key:                     'bg:#aad4ff #4f7aa4',Token.Toolbar.Status.PasteModeOn:             'bg:#7c63d1 #002a55',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#6690e8 #38638d',Token.Toolbar.Status.PythonVersion:           'bg:#93bee8 #002a55 bold',Token.Aborted:                                '#4f7aa4',Token.Sidebar:                                'bg:#2d5882 #aad4ff',Token.Sidebar.Title:                          'bg:#0090a4 #002a55 bold',Token.Sidebar.Label:                          'bg:#2d5882 #93bee8',Token.Sidebar.Status:                         'bg:#16416b #9ed4ff',Token.Sidebar.Selected.Label:                 'bg:#93bee8 #0b3660',Token.Sidebar.Selected.Status:                'bg:#7ca7d1 #002a55 bold',Token.Sidebar.Separator:                       'bg:#2d5882 #002a55 underline',Token.Sidebar.Key:                            'bg:#2d586b #aad4ff bold',Token.Sidebar.Key.Description:                'bg:#2d5882 #aad4ff',Token.Sidebar.HelpText:                       'bg:#003660 #9ed4ff',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#aad4a4  #aad4ff',Token.History.Line.Current:                  'bg:#002a55 #aad4ff',Token.History.Line.Selected.Current:         'bg:#4f7a55 #aad4ff',Token.History.ExistingInput:                  '#4f7aa4',Token.Window.Border:                          '#2dd4ff',Token.Window.Title:                           'bg:#2d5882 #aad4ff',Token.Window.TIItleV2:                         'bg:#2d90a4 #aad4ff bold',Token.AcceptMessage:                          'bg:#4f2a55 #7ca7d1',Token.ExitConfirmation:                       'bg:#7c7ad1 #002a55',}
cyan_2={Token.LineNumber:'#51bbb7 bg:#1b3381',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #0033d2',Token.In.Number:                              '',Token.Out:                                    '#00ff66',Token.Out.Number:                             '#00ff66',Token.Separator:                              '#95c8fb',Token.Toolbar.Search:                         '#884eee noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#884eee noinherit',Token.Toolbar.Arg:                            '#884eee noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#9569fb #003366',Token.Toolbar.Signature.CurrentName:          'bg:#6c33d2 #ccffff bold',Token.Toolbar.Signature.Operator:             '#003366 bold',Token.Docstring:                              '#6ca0d2',Token.Toolbar.Validation:                     'bg:#006966 #88bbee',Token.Toolbar.Status:                         'bg:#1b4e81 #88bbee',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#1b4e81 #1b4eee',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#1b4e81 #1bbb81',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#1b4e81 #88ffff',Token.Toolbar.Status.Key:                     'bg:#003366 #6ca0d2',Token.Toolbar.Status.PasteModeOn:             'bg:#36bb9c #ccffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#518481 #88bbee',Token.Toolbar.Status.PythonVersion:           'bg:#1b4e81 #ccffff bold',Token.Aborted:                                '#6ca0d2',Token.Sidebar:                                'bg:#95c8fb #003366',Token.Sidebar.Title:                          'bg:#cc84d2 #ccffff bold',Token.Sidebar.Label:                          'bg:#95c8fb #1b4e81',Token.Sidebar.Status:                         'bg:#b0e4ff #0d3366',Token.Sidebar.Selected.Label:                 'bg:#1b4e81 #bef1ff',Token.Sidebar.Selected.Status:                'bg:#36699c #ccffff bold',Token.Sidebar.Separator:                       'bg:#95c8fb #ccffff underline',Token.Sidebar.Key:                            'bg:#95c8ff #003366 bold',Token.Sidebar.Key.Description:                'bg:#95c8fb #003366',Token.Sidebar.HelpText:                       'bg:#ccf1ff #0d3366',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#0033d2  #003366',Token.History.Line.Current:                  'bg:#ccffff #003366',Token.History.Line.Selected.Current:         'bg:#6ca0ff #003366',Token.History.ExistingInput:                  '#6ca0d2',Token.Window.Border:                          '#953366',Token.Window.Title:                           'bg:#95c8fb #003366',Token.Window.TIItleV2:                         'bg:#9584d2 #003366 bold',Token.AcceptMessage:                          'bg:#6cffff #36699c',Token.ExitConfirmation:                       'bg:#36a09c #ccffff',}
cyan_3={Token.LineNumber:'#24d4ce bg:#000073',    Token.Prompt:                                 'bold',Token.Prompt.Dots:                            'noinherit',Token.In:                                     'bold #0000fb',Token.In.Number:                              '',Token.Out:                                    '#00ff46',Token.Out.Number:                             '#00ff46',Token.Separator:                              '#95eaff',Token.Toolbar.Search:                         '#7e1eff noinherit',Token.Toolbar.Search.Text:                    'noinherit',Token.Toolbar.System:                         '#7e1eff noinherit',Token.Toolbar.Arg:                            '#7e1eff noinherit',Token.Toolbar.Arg.Text:                       'noinherit',Token.Toolbar.Signature:                      'bg:#954cff #000046',Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',Token.Toolbar.Signature.Operator:             '#000046 bold',Token.Docstring:                              '#51a6fb',Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',Token.Toolbar.Status.Title:                   'underline',Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',Token.Aborted:                                '#51a6fb',Token.Sidebar:                                'bg:#95eaff #000046',Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',Token.Sidebar.Label:                          'bg:#95eaff #001e73',Token.Sidebar.Status:                         'bg:#c2ffff #000046',Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',Token.Sidebar.Key.Description:                'bg:#95eaff #000046',Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',Token.History.Line:                          '',Token.History.Line.Selected:                 'bg:#0000fb  #000046',Token.History.Line.Current:                  'bg:#f0ffff #000046',Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',Token.History.ExistingInput:                  '#51a6fb',Token.Window.Border:                          '#950046',Token.Window.Title:                           'bg:#95eaff #000046',Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',Token.AcceptMessage:                          'bg:#51ffff #004ca0',Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',}
cyan_4={    Token.LineNumber:'#24d4ce bg:#000073',    Token.Prompt:                                 'bold',    Token.Prompt.Dots:                            'noinherit',    Token.In:                                     'bold #0000fb',    Token.In.Number:                              '',    Token.Out:                                    '#00ff46',    Token.Out.Number:                             '#00ff46',    Token.Separator:                              '#95eaff',    Token.Toolbar.Search:                         '#7e1eff noinherit',    Token.Toolbar.Search.Text:                    'noinherit',    Token.Toolbar.System:                         '#7e1eff noinherit',    Token.Toolbar.Arg:                            '#7e1eff noinherit',    Token.Toolbar.Arg.Text:                       'noinherit',    Token.Toolbar.Signature:                      'bg:#954cff #000046',    Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',    Token.Toolbar.Signature.Operator:             '#000046 bold',    Token.Docstring:                              '#51a6fb',    Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',    Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',    Token.Toolbar.Status.Title:                   'underline',    Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',    Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',    Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',    Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',    Token.Aborted:                                '#51a6fb',    Token.Sidebar:                                'bg:#95eaff #000046',    Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',    Token.Sidebar.Label:                          'bg:#95eaff #001e73',    Token.Sidebar.Status:                         'bg:#c2ffff #000046',    Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',    Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',    Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',    Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',    Token.Sidebar.Key.Description:                'bg:#95eaff #000046',    Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',    Token.History.Line:                          '',    Token.History.Line.Selected:                 'bg:#0000fb  #000046',    Token.History.Line.Current:                  'bg:#f0ffff #000046',    Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',    Token.History.ExistingInput:                  '#51a6fb',    Token.Window.Border:                          '#950046',    Token.Window.Title:                           'bg:#95eaff #000046',    Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',    Token.AcceptMessage:                          'bg:#51ffff #004ca0',    Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',    Token.LineNumber:                             '#24d4ce bg:#001e73',        Token.SearchMatch:                            '#f0ffff bg:#7e4ca0',        Token.SearchMatch.Current:                    '#f0ffff bg:#004cff',        Token.SelectedText:                           '#f0ffff bg:#7e79ce',        Token.Toolbar.Completions:                    'bg:#954cff #000046',        Token.Toolbar.Completions.Arrow:              'bg:#954cff #000046 bold',        Token.Toolbar.Completions.Completion:         'bg:#954cff #000046',        Token.Toolbar.Completions.Completion.Current: 'bg:#5100fb #f0ffff',        Token.Menu.Completions.Completion:            'bg:#954cff #000046',        Token.Menu.Completions.Completion.Current:    'bg:#5100fb #f0ffff',        Token.Menu.Completions.Meta:                  'bg:#684cff #000046',        Token.Menu.Completions.Meta.Current:          'bg:#7e00ff #000046',        Token.Menu.Completions.ProgressBar:           'bg:#7ed4ff',        Token.Menu.Completions.ProgressButton:        'bg:#000046',}
cyan_4={    
     Token.LineNumber:                                  '    #24d4ce        bg:#000073                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #0000fb                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #00ff46                                       ',
     Token.Out.Number:                                  '    #00ff46                                       ',
     Token.Separator:                                   '    #95eaff                                       ',
     Token.Toolbar.Search:                              '    #7e1eff                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #7e1eff                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #7e1eff                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #000046        bg:#954cff                     ',
     Token.Toolbar.Signature.CurrentName:               '    #f0ffff        bg:#5100fb        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #000046                          bold         ',
     Token.Docstring:                                   '    #51a6fb                                       ',
     Token.Toolbar.Validation:                          '    #7ed4ff        bg:#004c46                     ',
     Token.Toolbar.Status:                              '    #7ed4ff        bg:#001e73                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #7effff        bg:#001e73                     ',
     Token.Toolbar.Status.Key:                          '    #51a6fb        bg:#000046                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #f0ffff        bg:#00d4a0                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #7ed4ff        bg:#247973                     ',
     Token.Toolbar.Status.PythonVersion:                '    #f0ffff        bg:#001e73        bold         ',
     Token.Aborted:                                     '    #51a6fb                                       ',
     Token.Sidebar:                                     '    #000046        bg:#95eaff                     ',
     Token.Sidebar.Title:                               '    #f0ffff        bg:#f079fb        bold         ',
     Token.Sidebar.Label:                               '    #001e73        bg:#95eaff                     ',
     Token.Sidebar.Status:                              '    #000046        bg:#c2ffff                     ',
     Token.Sidebar.Selected.Label:                      '    #d9ffff        bg:#001e73                     ',
     Token.Sidebar.Selected.Status:                     '    #f0ffff        bg:#004ca0        bold         ',
     Token.Sidebar.Separator:                           '    #f0ffff        bg:#95eaff        underline    ',
     Token.Sidebar.Key:                                 '    #000046        bg:#95eaff        bold         ',
     Token.Sidebar.Key.Description:                     '    #000046        bg:#95eaff                     ',
     Token.Sidebar.HelpText:                            '    #000046        bg:#a0f0ff                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #000046        bg:#0000fb                     ',
     Token.History.Line.Current:                        '    #000046        bg:#f0ffff                     ',
     Token.History.Line.Selected.Current:               '    #000046        bg:#51a6ff                     ',
     Token.History.ExistingInput:                       '    #51a6fb                                       ',
     Token.Window.Border:                               '    #950046                                       ',
     Token.Window.Title:                                '    #000046        bg:#95eaff                     ',
     Token.Window.TIItleV2:                             '    #000046        bg:#9579fb        bold         ',
     Token.AcceptMessage:                               '    #004ca0        bg:#51ffff                     ',
     Token.ExitConfirmation:                            '    #f0ffff        bg:#00a6a0                     ',
     Token.LineNumber:                                  '    #24d4ce        bg:#001e73                     ',
     Token.SearchMatch:                                 '    #f0ffff        bg:#7e4ca0                     ',
     Token.SearchMatch.Current:                         '    #f0ffff        bg:#004cff                     ',
     Token.SelectedText:                                '    #f0ffff        bg:#7e79ce                     ',
     Token.Toolbar.Completions:                         '    #000046        bg:#954cff                     ',
     Token.Toolbar.Completions.Arrow:                   '    #000046        bg:#954cff        bold         ',
     Token.Toolbar.Completions.Completion:              '    #000046        bg:#954cff                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #f0ffff        bg:#5100fb                     ',
     Token.Menu.Completions.Completion:                 '    #000046        bg:#954cff                     ',
     Token.Menu.Completions.Completion.Current:         '    #f0ffff        bg:#5100fb                     ',
     Token.Menu.Completions.Meta:                       '    #000046        bg:#684cff                     ',
     Token.Menu.Completions.Meta.Current:               '    #000046        bg:#7e00ff                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#7ed4ff                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#000046                     ',
}



cyan_4__02={    
     Token.LineNumber:                                  '    #ce24d4        bg:#730000                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #fb0000                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #4600ff                                       ',
     Token.Out.Number:                                  '    #4600ff                                       ',
     Token.Separator:                                   '    #ff95ea                                       ',
     Token.Toolbar.Search:                              '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #ff7e1e                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fff0ff        bg:#fb5100        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #460000                          bold         ',
     Token.Docstring:                                   '    #fb51a6                                       ',
     Token.Toolbar.Validation:                          '    #ff7ed4        bg:#46004c                     ',
     Token.Toolbar.Status:                              '    #ff7ed4        bg:#73001e                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ff7eff        bg:#73001e                     ',
     Token.Toolbar.Status.Key:                          '    #fb51a6        bg:#460000                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fff0ff        bg:#a000d4                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #ff7ed4        bg:#732479                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fff0ff        bg:#73001e        bold         ',
     Token.Aborted:                                     '    #fb51a6                                       ',
     Token.Sidebar:                                     '    #460000        bg:#ff95ea                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#fbf079        bold         ',
     Token.Sidebar.Label:                               '    #73001e        bg:#ff95ea                     ',
     Token.Sidebar.Status:                              '    #460000        bg:#ffc2ff                     ',
     Token.Sidebar.Selected.Label:                      '    #ffd9ff        bg:#73001e                     ',
     Token.Sidebar.Selected.Status:                     '    #ffffff        bg:#a0004c        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#ff95ea        underline    ',
     Token.Sidebar.Key:                                 '    #460000        bg:#ff95ea        bold         ',
     Token.Sidebar.Key.Description:                     '    #460000        bg:#ff95ea                     ',
     Token.Sidebar.HelpText:                            '    #460000        bg:#ffa0f0                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #460000        bg:#fb0000                     ',
     Token.History.Line.Current:                        '    #460000        bg:#fff0ff                     ',
     Token.History.Line.Selected.Current:               '    #460000        bg:#ff51a6                     ',
     Token.History.ExistingInput:                       '    #fb51a6                                       ',
     Token.Window.Border:                               '    #469500                                       ',
     Token.Window.Title:                                '    #460000        bg:#ff95ea                     ',
     Token.Window.TIItleV2:                             '    #460000        bg:#fb9579        bold         ',
     Token.AcceptMessage:                               '    #a0004c        bg:#ff51ff                     ',
     Token.ExitConfirmation:                            '    #fff0ff        bg:#a000a6                     ',
     Token.LineNumber:                                  '    #ce24d4        bg:#73001e                     ',
     Token.SearchMatch:                                 '    #fff0ff        bg:#a07e4c                     ',
     Token.SearchMatch.Current:                         '    #fff0ff        bg:#ff004c                     ',
     Token.SelectedText:                                '    #fff0ff        bg:#ce7e79                     ',
     Token.Toolbar.Completions:                         '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Completions.Arrow:                   '    #460000        bg:#ff954c        bold         ',
     Token.Toolbar.Completions.Completion:              '    #460000        bg:#ff954c                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #fff0ff        bg:#fb5100                     ',
     Token.Menu.Completions.Completion:                 '    #460000        bg:#ff954c                     ',
     Token.Menu.Completions.Completion.Current:         '    #fff0ff        bg:#fb5100                     ',
     Token.Menu.Completions.Meta:                       '    #460000        bg:#ff684c                     ',
     Token.Menu.Completions.Meta.Current:               '    #460000        bg:#ff7e00                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#ff7ed4                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#460000                     ',
}






cyan_4__02__02={    
     Token.LineNumber:                                  '    #d4ce24        bg:#007300                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #00fb00                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #ff4600                                       ',
     Token.Out.Number:                                  '    #ff4600                                       ',
     Token.Separator:                                   '    #eaff95                                       ',
     Token.Toolbar.Search:                              '    #1eff7e                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #1eff7e                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #1eff7e                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fffff0        bg:#00fb51        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #004600                          bold         ',
     Token.Docstring:                                   '    #a6fb51                                       ',
     Token.Toolbar.Validation:                          '    #d4ff7e        bg:#4c4600                     ',
     Token.Toolbar.Status:                              '    #d4ff7e        bg:#1e7300                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ffff7e        bg:#1e7300                     ',
     Token.Toolbar.Status.Key:                          '    #a6fb51        bg:#004600                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fffff0        bg:#d4a000                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #d4ff7e        bg:#797324                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fffff0        bg:#1e7300        bold         ',
     Token.Aborted:                                     '    #a6fb51                                       ',
     Token.Sidebar:                                     '    #004600        bg:#eaff95                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#79fbf0        bold         ',
     Token.Sidebar.Label:                               '    #1e7300        bg:#eaff95                     ',
     Token.Sidebar.Status:                              '    #004600        bg:#ffffc2                     ',
     Token.Sidebar.Selected.Label:                      '    #ffffd9        bg:#1e7300                     ',
     Token.Sidebar.Selected.Status:                     '    #000000        bg:#4ca000        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#eaff95        underline    ',
     Token.Sidebar.Key:                                 '    #004600        bg:#eaff95        bold         ',
     Token.Sidebar.Key.Description:                     '    #004600        bg:#eaff95                     ',
     Token.Sidebar.HelpText:                            '    #004600        bg:#f0ffa0                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #004600        bg:#00fb00                     ',
     Token.History.Line.Current:                        '    #004600        bg:#fffff0                     ',
     Token.History.Line.Selected.Current:               '    #004600        bg:#a6ff51                     ',
     Token.History.ExistingInput:                       '    #a6fb51                                       ',
     Token.Window.Border:                               '    #004695                                       ',
     Token.Window.Title:                                '    #004600        bg:#eaff95                     ',
     Token.Window.TIItleV2:                             '    #004600        bg:#79fb95        bold         ',
     Token.AcceptMessage:                               '    #4ca000        bg:#ffff51                     ',
     Token.ExitConfirmation:                            '    #fffff0        bg:#a6a000                     ',
     Token.LineNumber:                                  '    #d4ce24        bg:#1e7300                     ',
     Token.SearchMatch:                                 '    #fffff0        bg:#4ca07e                     ',
     Token.SearchMatch.Current:                         '    #fffff0        bg:#4cff00                     ',
     Token.SelectedText:                                '    #fffff0        bg:#79ce7e                     ',
     Token.Toolbar.Completions:                         '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Completions.Arrow:                   '    #004600        bg:#4cff95        bold         ',
     Token.Toolbar.Completions.Completion:              '    #004600        bg:#4cff95                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #fffff0        bg:#00fb51                     ',
     Token.Menu.Completions.Completion:                 '    #004600        bg:#4cff95                     ',
     Token.Menu.Completions.Completion.Current:         '    #fffff0        bg:#00fb51                     ',
     Token.Menu.Completions.Meta:                       '    #004600        bg:#4cff68                     ',
     Token.Menu.Completions.Meta.Current:               '    #004600        bg:#00ff7e                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#d4ff7e                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#004600                     ',
}




cyan_4__02__02__12={    
     Token.LineNumber:                                  '    #d424ce        bg:#000073                     ',
     Token.Prompt:                                      '                                     bold         ',
     Token.Prompt.Dots:                                 '                                     noinherit    ',
     Token.In:                                          '    #0000fb                          bold         ',
     Token.In.Number:                                   '                                                  ',
     Token.Out:                                         '    #ff0046                                       ',
     Token.Out.Number:                                  '    #ff0046                                       ',
     Token.Separator:                                   '    #ea95ff                                       ',
     Token.Toolbar.Search:                              '    #1e7eff                          noinherit    ',
     Token.Toolbar.Search.Text:                         '                                     noinherit    ',
     Token.Toolbar.System:                              '    #1e7eff                          noinherit    ',
     Token.Toolbar.Arg:                                 '    #1e7eff                          noinherit    ',
     Token.Toolbar.Arg.Text:                            '                                     noinherit    ',
     Token.Toolbar.Signature:                           '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Signature.CurrentName:               '    #fff0ff        bg:#0051fb        bold         ',
     Token.Toolbar.Signature.Operator:                  '    #000046                          bold         ',
     Token.Docstring:                                   '    #a651fb                                       ',
     Token.Toolbar.Validation:                          '    #d47eff        bg:#4c0046                     ',
     Token.Toolbar.Status:                              '    #d47eff        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryPluggedIn:             '    #aaff55        bg:#1e0073                     ',
     Token.Toolbar.Status.BatteryNotPluggedIn:          '    #ff55aa        bg:#1e0073                     ',
     Token.Toolbar.Status.Title:                        '                                     underline    ',
     Token.Toolbar.Status.InputMode:                    '    #ff7eff        bg:#1e0073                     ',
     Token.Toolbar.Status.Key:                          '    #a651fb        bg:#000046                     ',
     Token.Toolbar.Status.PasteModeOn:                  '    #fff0ff        bg:#d400a0                     ',
     Token.Toolbar.Status.PseudoTerminalCurrentVariable:'    #d47eff        bg:#792473                     ',
     Token.Toolbar.Status.PythonVersion:                '    #fff0ff        bg:#1e0073        bold         ',
     Token.Aborted:                                     '    #a651fb                                       ',
     Token.Sidebar:                                     '    #000046        bg:#ea95ff                     ',
     Token.Sidebar.Title:                               '    #000000        bg:#79f0fb        bold         ',
     Token.Sidebar.Label:                               '    #1e0073        bg:#ea95ff                     ',
     Token.Sidebar.Status:                              '    #000046        bg:#ffc2ff                     ',
     Token.Sidebar.Selected.Label:                      '    #ffd9ff        bg:#1e0073                     ',
     Token.Sidebar.Selected.Status:                     '    #FFFFFF        bg:#4c00a0        bold         ',
     Token.Sidebar.Separator:                           '    #000000        bg:#ea95ff        underline    ',
     Token.Sidebar.Key:                                 '    #000046        bg:#ea95ff        bold         ',
     Token.Sidebar.Key.Description:                     '    #000046        bg:#ea95ff                     ',
     Token.Sidebar.HelpText:                            '    #000046        bg:#f0a0ff                     ',
     Token.History.Line:                                '                                                  ',
     Token.History.Line.Selected:                       '    #000046        bg:#0000fb                     ',
     Token.History.Line.Current:                        '    #000046        bg:#fff0ff                     ',
     Token.History.Line.Selected.Current:               '    #000046        bg:#a651ff                     ',
     Token.History.ExistingInput:                       '    #a651fb                                       ',
     Token.Window.Border:                               '    #009546                                       ',
     Token.Window.Title:                                '    #000046        bg:#ea95ff                     ',
     Token.Window.TIItleV2:                             '    #000046        bg:#7995fb        bold         ',
     Token.AcceptMessage:                               '    #4c00a0        bg:#ff51ff                     ',
     Token.ExitConfirmation:                            '    #fff0ff        bg:#a600a0                     ',
     Token.LineNumber:                                  '    #d424ce        bg:#1e0073                     ',
     Token.SearchMatch:                                 '    #fff0ff        bg:#4c7ea0                     ',
     Token.SearchMatch.Current:                         '    #fff0ff        bg:#4c00ff                     ',
     Token.SelectedText:                                '    #fff0ff        bg:#797ece                     ',
     Token.Toolbar.Completions:                         '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Completions.Arrow:                   '    #000046        bg:#4c95ff        bold         ',
     Token.Toolbar.Completions.Completion:              '    #000046        bg:#4c95ff                     ',
     Token.Toolbar.Completions.Completion.Current:      '    #fff0ff        bg:#0051fb                     ',
     Token.Menu.Completions.Completion:                 '    #000046        bg:#4c95ff                     ',
     Token.Menu.Completions.Completion.Current:         '    #fff0ff        bg:#0051fb                     ',
     Token.Menu.Completions.Meta:                       '    #000046        bg:#4c68ff                     ',
     Token.Menu.Completions.Meta.Current:               '    #000046        bg:#007eff                     ',
     Token.Menu.Completions.ProgressBar:                '                   bg:#d47eff                     ',
     Token.Menu.Completions.ProgressButton:             '                   bg:#000046                     ',
}




temp = {
    Token.LineNumber:'#24d4ce bg:#000073',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #0000fb',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#00ff46',
    Token.Out.Number:                             '#00ff46',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#95eaff',

    # Search toolbar.
    Token.Toolbar.Search:                         '#7e1eff noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#7e1eff noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#7e1eff noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#954cff #000046',
    Token.Toolbar.Signature.CurrentName:          'bg:#5100fb #f0ffff bold',
    Token.Toolbar.Signature.Operator:             '#000046 bold',

    Token.Docstring:                              '#51a6fb',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#004c46 #7ed4ff',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#001e73 #7ed4ff',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#001e73 #001eff',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#001e73 #00d473',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#001e73 #7effff',
    Token.Toolbar.Status.Key:                     'bg:#000046 #51a6fb',
    Token.Toolbar.Status.PasteModeOn:             'bg:#00d4a0 #f0ffff',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#247973 #7ed4ff',
    Token.Toolbar.Status.PythonVersion:           'bg:#001e73 #f0ffff bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#51a6fb',

    # The options sidebar.
    Token.Sidebar:                                'bg:#95eaff #000046',
    Token.Sidebar.Title:                          'bg:#f079fb #f0ffff bold',
    Token.Sidebar.Label:                          'bg:#95eaff #001e73',
    Token.Sidebar.Status:                         'bg:#c2ffff #000046',
    Token.Sidebar.Selected.Label:                 'bg:#001e73 #d9ffff',
    Token.Sidebar.Selected.Status:                'bg:#004ca0 #f0ffff bold',

    Token.Sidebar.Separator:                       'bg:#95eaff #f0ffff underline',
    Token.Sidebar.Key:                            'bg:#95eaff #000046 bold',
    Token.Sidebar.Key.Description:                'bg:#95eaff #000046',
    Token.Sidebar.HelpText:                       'bg:#f0ffff #000046',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#0000fb  #000046',
    Token.History.Line.Current:                  'bg:#f0ffff #000046',
    Token.History.Line.Selected.Current:         'bg:#51a6ff #000046',
    Token.History.ExistingInput:                  '#51a6fb',

    # Help Window.
    Token.Window.Border:                          '#950046',
    Token.Window.Title:                           'bg:#95eaff #000046',
    Token.Window.TIItleV2:                         'bg:#9579fb #000046 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#51ffff #004ca0',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#00a6a0 #f0ffff',
}
temp.update({
    Token.Aborted:                                '#3a90e4',
    Token.Sidebar:                                'bg:#004ca0 #f0ffff',
    Token.Sidebar.Title:                          'bg:#00bde4 #000046 bold',
    Token.Sidebar.Label:                          'bg:#004ca0 #c2ffff',
    Token.Sidebar.Status:                         'bg:#001e73 #d9ffff',
    Token.Sidebar.Selected.Label:                 'bg:#c2ffff #00085c',
    Token.Sidebar.Selected.Status:                'bg:#95eaff #000046 bold',
    Token.Sidebar.Separator:                       'bg:#004ca0 #000046 underline',
    Token.Sidebar.Key:                            'bg:#004c73 #f0ffff bold',
    Token.Sidebar.Key.Description:                'bg:#004ca0 #f0ffff',
    Token.Sidebar.HelpText:                       'bg:#00085c #d9ffff',
    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#f0ffe4  #f0ffff',
    Token.History.Line.Current:                  'bg:#000046 #f0ffff',
    Token.History.Line.Selected.Current:         'bg:#3a9046 #f0ffff',
    Token.History.ExistingInput:                  '#3a90e4',
    # Help Window.
    Token.Window.Border:                          '#00ffff',
    Token.Window.Title:                           'bg:#004ca0 #f0ffff',
    Token.Window.TIItleV2:                         'bg:#00bde4 #f0ffff bold',
    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#3a0046 #95eaff',
    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#9590ff #000046',
    # Line numbers.
    Token.LineNumber:                             '#24d4ce bg:#001e73',
    # Highlighting of search matches in document.
    Token.SearchMatch:                            '#f0ffff bg:#7e4ca0',
    Token.SearchMatch.Current:                    '#f0ffff bg:#004cff',
    # Highlighting of select text in document.
    Token.SelectedText:                           '#f0ffff bg:#7e79ce',
    Token.Toolbar.Completions:            'bg:#000046 #01f0ff',
    Token.Toolbar.Completions.Arrow:              'bg:#000046 #01f0ff bold',
    Token.Toolbar.Completions.Completion:         'bg:#000046 #01f0ff',
    Token.Toolbar.Completions.Completion.Current: 'bg:#f0ffff #007eb2',
    # Completer menu.
    Token.Menu.Completions.Completion:            'bg:#000046 #01ffff',
    Token.Menu.Completions.Completion.Current:    'bg:#f0ffff #00ffb2',
    Token.Menu.Completions.Meta:                  'bg:#000046 #01ffd0',
    Token.Menu.Completions.Meta.Current:          'bg:#000046 #00ffee',
    Token.Menu.Completions.ProgressBar:           'bg:#b6ffee           ',
    Token.Menu.Completions.ProgressButton:        'bg:#004e46           ',
})
newstyle=temp





temp = {
    Token.LineNumber:'#d3cd23 bg:#007200',
    # Classic prompt.
    Token.Prompt:                                 'bold',
    Token.Prompt.Dots:                            'noinherit',

    # (IPython <5.0) Prompt: "In [1]:"
    Token.In:                                     'bold #00fa00',
    Token.In.Number:                              '',

    # Return value.
    Token.Out:                                    '#fe4500',
    Token.Out.Number:                             '#fe4500',

    # Separator between windows. (Used above docstring.)
    Token.Separator:                              '#e9fe94',

    # Search toolbar.
    Token.Toolbar.Search:                         '#1dfe7d noinherit',
    Token.Toolbar.Search.Text:                    'noinherit',

    # System toolbar
    Token.Toolbar.System:                         '#1dfe7d noinherit',

    # "arg" toolbar.
    Token.Toolbar.Arg:                            '#1dfe7d noinherit',
    Token.Toolbar.Arg.Text:                       'noinherit',

    # Signature toolbar.
    Token.Toolbar.Signature:                      'bg:#4bfe94 #004500',
    Token.Toolbar.Signature.CurrentName:          'bg:#00fa50 #fefeef bold',
    Token.Toolbar.Signature.Operator:             '#004500 bold',

    Token.Docstring:                              '#a5fa50',

    # Validation toolbar.
    Token.Toolbar.Validation:                     'bg:#4b4500 #d3fe7d',

    # Status toolbar.
    Token.Toolbar.Status:                         'bg:#1d7200 #d3fe7d',
    Token.Toolbar.Status.BatteryPluggedIn:        'bg:#1d7200 #1dfe00',
    Token.Toolbar.Status.BatteryNotPluggedIn:     'bg:#1d7200 #d37200',
    Token.Toolbar.Status.Title:                   'underline',
    Token.Toolbar.Status.InputMode:               'bg:#1d7200 #fefe7d',
    Token.Toolbar.Status.Key:                     'bg:#004500 #a5fa50',
    Token.Toolbar.Status.PasteModeOn:             'bg:#d39f00 #fefeef',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:'bg:#787223 #d3fe7d',
    Token.Toolbar.Status.PythonVersion:           'bg:#1d7200 #fefeef bold',

    # When Control-C has been pressed. Grayed.
    Token.Aborted:                                '#a5fa50',

    # The options sidebar.
    Token.Sidebar:                                'bg:#e9fe94 #004500',
    Token.Sidebar.Title:                          'bg:#78faef #fefeef bold',
    Token.Sidebar.Label:                          'bg:#e9fe94 #1d7200',
    Token.Sidebar.Status:                         'bg:#fefec1 #004500',
    Token.Sidebar.Selected.Label:                 'bg:#1d7200 #fefed8',
    Token.Sidebar.Selected.Status:                'bg:#4b9f00 #fefeef bold',

    Token.Sidebar.Separator:                       'bg:#e9fe94 #fefeef underline',
    Token.Sidebar.Key:                            'bg:#e9fe94 #004500 bold',
    Token.Sidebar.Key.Description:                'bg:#e9fe94 #004500',
    Token.Sidebar.HelpText:                       'bg:#fefeef #004500',

    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#00fa00  #004500',
    Token.History.Line.Current:                  'bg:#fefeef #004500',
    Token.History.Line.Selected.Current:         'bg:#a5fe50 #004500',
    Token.History.ExistingInput:                  '#a5fa50',

    # Help Window.
    Token.Window.Border:                          '#004594',
    Token.Window.Title:                           'bg:#e9fe94 #004500',
    Token.Window.TIItleV2:                         'bg:#78fa94 #004500 bold',

    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#fefe50 #4b9f00',

    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#a59f00 #fefeef',
}
temp.update({
    Token.Aborted:                                '#8fe339',
    Token.Sidebar:                                'bg:#4b9f00 #fefeef',
    Token.Sidebar.Title:                          'bg:#bce300 #004500 bold',
    Token.Sidebar.Label:                          'bg:#4b9f00 #fefec1',
    Token.Sidebar.Status:                         'bg:#1d7200 #fefed8',
    Token.Sidebar.Selected.Label:                 'bg:#fefec1 #075b00',
    Token.Sidebar.Selected.Status:                'bg:#e9fe94 #004500 bold',
    Token.Sidebar.Separator:                       'bg:#4b9f00 #004500 underline',
    Token.Sidebar.Key:                            'bg:#4b7200 #fefeef bold',
    Token.Sidebar.Key.Description:                'bg:#4b9f00 #fefeef',
    Token.Sidebar.HelpText:                       'bg:#075b00 #fefed8',
    # Styling for the history layout.
    Token.History.Line:                          '',
    Token.History.Line.Selected:                 'bg:#fee3ef  #fefeef',
    Token.History.Line.Current:                  'bg:#004500 #fefeef',
    Token.History.Line.Selected.Current:         'bg:#8f4539 #fefeef',
    Token.History.ExistingInput:                  '#8fe339',
    # Help Window.
    Token.Window.Border:                          '#fefe00',
    Token.Window.Title:                           'bg:#4b9f00 #fefeef',
    Token.Window.TIItleV2:                         'bg:#bce300 #fefeef bold',
    # Meta-enter message.
    Token.AcceptMessage:                          'bg:#004539 #e9fe94',
    # Exit confirmation.
    Token.ExitConfirmation:                       'bg:#8ffe94 #004500',
    # Line numbers.
    Token.LineNumber:                             '#d3cd23 bg:#1d7200',
    # Highlighting of search matches in document.
    Token.SearchMatch:                            '#fefeef bg:#4b9f7d',
    Token.SearchMatch.Current:                    '#fefeef bg:#4bfe00',
    # Highlighting of select text in document.
    Token.SelectedText:                           '#fefeef bg:#78cd7d',
    Token.Toolbar.Completions:                    'bg:#004500 #effe00',
    Token.Toolbar.Completions.Arrow:              'bg:#004500 #effe00 bold',
    Token.Toolbar.Completions.Completion:         'bg:#004500 #effe00',
    Token.Toolbar.Completions.Completion.Current: 'bg:#fefeef #7db100',
    # Completer menu.
    Token.Menu.Completions.Completion:            'bg:#004500 #fefe00',
    Token.Menu.Completions.Completion.Current:    'bg:#fefeef #feb100',
    Token.Menu.Completions.Meta:                  'bg:#004500 #fecf00',
    Token.Menu.Completions.Meta.Current:          'bg:#004500 #feed00',
    Token.Menu.Completions.ProgressBar:           'bg:#feedb5           ',
    Token.Menu.Completions.ProgressButton:        'bg:#4d4500           ',
})
dejavu=temp





temp = {
    Token.LineNumber:'bg:#007200 #d3cd23',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #0000fa bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #fe0045',
    Token.Out.Number:                                     '           #fe0045',
    Token.Separator:                                      '           #e994fe',
    Token.Toolbar.Search:                                 '           #1d7dfe noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #1d7dfe noinherit',
    Token.Toolbar.Arg:                                    '           #1d7dfe noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#4b94fe #000045',
    Token.Toolbar.Signature.CurrentName:                  'bg:#0050fa #feeffe bold',
    Token.Toolbar.Signature.Operator:                     '           #000045            bold',
    Token.Docstring:                                      '           #a550fa',
    Token.Toolbar.Validation:                             'bg:#4b0045 #d37dfe',
    Token.Toolbar.Status:                                 'bg:#1d0072 #d37dfe',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#1d0072 #1d00fe',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#1d0072 #d30072',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#1d0072 #fe7dfe',
    Token.Toolbar.Status.Key:                             'bg:#000045 #a550fa',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#d3009f #feeffe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#782372 #d37dfe',
    Token.Toolbar.Status.PythonVersion:                   'bg:#1d0072 #feeffe bold',
    Token.Aborted:                                        '           #a550fa',
    Token.Sidebar:                                        'bg:#e994fe #000045',
    Token.Sidebar.Title:                                  'bg:#78effa #feeffe bold',
    Token.Sidebar.Label:                                  'bg:#e994fe #1d0072',
    Token.Sidebar.Status:                                 'bg:#fec1fe #000045',
    Token.Sidebar.Selected.Label:                         'bg:#1d0072 #fed8fe',
    Token.Sidebar.Selected.Status:                        'bg:#4b009f #feeffe bold',
    Token.Sidebar.Separator:                              'bg:#e994fe #feeffe underline',
    Token.Sidebar.Key:                                    'bg:#e994fe #000045 bold',
    Token.Sidebar.Key.Description:                        'bg:#e994fe #000045',
    Token.Sidebar.HelpText:                               'bg:#feeffe #000045',
    Token.History.Line:                                   '',                        
    Token.History.Line.Selected:                          'bg:#0000fa #000045',
    Token.History.Line.Current:                           'bg:#feeffe #000045',
    Token.History.Line.Selected.Current:                  'bg:#a550fe #000045',
    Token.History.ExistingInput:                          '           #a550fa',
    Token.Window.Border:                                  '           #009445',
    Token.Window.Title:                                   'bg:#e994fe #000045',
    Token.Window.TIItleV2:                                'bg:#7894fa #000045 bold',
    Token.AcceptMessage:                                  'bg:#fe50fe #4b009f',
    Token.ExitConfirmation:                               'bg:#a5009f #feeffe',
}                                                                                                
temp.update({                                                                                                
    Token.Aborted:                                        '           #8fe339',                      
    Token.Sidebar:                                        'bg:#4b009f #feeffe',
    Token.Sidebar.Title:                                  'bg:#bc00e3 #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#4b009f #fec1fe',
    Token.Sidebar.Status:                                 'bg:#1d0072 #fed8fe',
    Token.Sidebar.Selected.Label:                         'bg:#fec1fe #07005b',
    Token.Sidebar.Selected.Status:                        'bg:#e994fe #000045 bold',
    Token.Sidebar.Separator:                              'bg:#4b009f #000045 underline',
    Token.Sidebar.Key:                                    'bg:#4b0072 #feeffe bold',
    Token.Sidebar.Key.Description:                        'bg:#4b009f #feeffe',
    Token.Sidebar.HelpText:                               'bg:#07005b #fed8fe',
    Token.History.Line:                                   '',                       
    Token.History.Line.Selected:                          'bg:#feefe3 #feeffe',
    Token.History.Line.Current:                           'bg:#000045 #feeffe',
    Token.History.Line.Selected.Current:                  'bg:#8f3945 #feeffe',
    Token.History.ExistingInput:                          '           #8f39e3',
    Token.Window.Border:                                  '           #fe00fe',
    Token.Window.Title:                                   'bg:#4b009f #feeffe',
    Token.Window.TIItleV2:                                'bg:#bc00e3 #feeffe bold',
    Token.AcceptMessage:                                  'bg:#003945 #e994fe',
    Token.ExitConfirmation:                               'bg:#8f94fe #000045',
    Token.LineNumber:                                     'bg:#1d0072 #d323cd',
    Token.SearchMatch:                                    'bg:#4b7d9f #feeffe',
    Token.SearchMatch.Current:                            'bg:#4b00fe #feeffe',
    Token.SelectedText:                                   'bg:#787dcd #feeffe',
    Token.Toolbar.Completions:                            'bg:#000045 #ef00fe',
    Token.Toolbar.Completions.Arrow:                      'bg:#000045 #ef00fe bold',
    Token.Toolbar.Completions.Completion:                 'bg:#000045 #ef00fe',
    Token.Toolbar.Completions.Completion.Current:         'bg:#feeffe #7d00b1',
    Token.Menu.Completions.Completion:                    'bg:#000045 #fe00fe',
    Token.Menu.Completions.Completion.Current:            'bg:#feeffe #fe00b1',
    Token.Menu.Completions.Meta:                          'bg:#000045 #fe00cf',
    Token.Menu.Completions.Meta.Current:                  'bg:#000045 #fe00ed',
    Token.Menu.Completions.ProgressBar:                   'bg:#feb5ed           ',
    Token.Menu.Completions.ProgressButton:                'bg:#4d0045           ',
})
sprice=temp



temp = {
    Token.LineNumber:                                     'bg:#000072 #23d3cd',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fa0000 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #45fe00',
    Token.Out.Number:                                     '           #45fe00',
    Token.Separator:                                      '           #fee994',
    Token.Toolbar.Search:                                 '           #fe1d7d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fe1d7d noinherit',
    Token.Toolbar.Arg:                                    '           #fe1d7d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fe4b94 #450000',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fa0050 #fefeef bold',
    Token.Toolbar.Signature.Operator:                     '           #450000            bold',
    Token.Docstring:                                      '           #faa550',
    Token.Toolbar.Validation:                             'bg:#454b00 #fed37d',
    Token.Toolbar.Status:                                 'bg:#721d00 #fed37d',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#721d00 #fe1d00',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#721d00 #72d300',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#721d00 #fefe7d',
    Token.Toolbar.Status.Key:                             'bg:#450000 #faa550',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9fd300 #fefeef',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#727823 #fed37d',
    Token.Toolbar.Status.PythonVersion:                   'bg:#721d00 #fefeef bold',
    Token.Aborted:                                        '           #faa550',
    Token.Sidebar:                                        'bg:#fee994 #450000',
    Token.Sidebar.Title:                                  'bg:#fa78ef #fefeef bold',
    Token.Sidebar.Label:                                  'bg:#fee994 #721d00',
    Token.Sidebar.Status:                                 'bg:#fefec1 #450000',
    Token.Sidebar.Selected.Label:                         'bg:#721d00 #fefed8',
    Token.Sidebar.Selected.Status:                        'bg:#9f4b00 #fefeef bold',
    Token.Sidebar.Separator:                              'bg:#fee994 #fefeef underline',
    Token.Sidebar.Key:                                    'bg:#fee994 #450000 bold',
    Token.Sidebar.Key.Description:                        'bg:#fee994 #450000',
    Token.Sidebar.HelpText:                               'bg:#fefeef #450000',
    Token.History.Line:                                   '',                        
    Token.History.Line.Selected:                          'bg:#fa0000 #450000',
    Token.History.Line.Current:                           'bg:#fefeef #450000',
    Token.History.Line.Selected.Current:                  'bg:#fea550 #450000',
    Token.History.ExistingInput:                          '           #faa550',
    Token.Window.Border:                                  '           #450094',
    Token.Window.Title:                                   'bg:#fee994 #450000',
    Token.Window.TIItleV2:                                'bg:#fa7894 #450000 bold',
    Token.AcceptMessage:                                  'bg:#fefe50 #9f4b00',
    Token.ExitConfirmation:                               'bg:#9fa500 #fefeef',
}                                                                                                
temp.update({                                                                                                
    Token.Aborted:                                        '           #398fe3',                      
    Token.Sidebar:                                        'bg:#9f4b00 #fefeef',
    Token.Sidebar.Title:                                  'bg:#e3bc00 #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#9f4b00 #fefec1',
    Token.Sidebar.Status:                                 'bg:#721d00 #fefed8',
    Token.Sidebar.Selected.Label:                         'bg:#fefec1 #5b0700',
    Token.Sidebar.Selected.Status:                        'bg:#fee994 #450000 bold',
    Token.Sidebar.Separator:                              'bg:#9f4b00 #450000 underline',
    Token.Sidebar.Key:                                    'bg:#724b00 #fefeef bold',
    Token.Sidebar.Key.Description:                        'bg:#9f4b00 #fefeef',
    Token.Sidebar.HelpText:                               'bg:#5b0700 #fefed8',
    Token.History.Line:                                   '',                       
    Token.History.Line.Selected:                          'bg:#e3feef #fefeef',
    Token.History.Line.Current:                           'bg:#450000 #fefeef',
    Token.History.Line.Selected.Current:                  'bg:#458f39 #fefeef',
    Token.History.ExistingInput:                          '           #e38f39',
    Token.Window.Border:                                  '           #fefe00',
    Token.Window.Title:                                   'bg:#9f4b00 #fefeef',
    Token.Window.TIItleV2:                                'bg:#e3bc00 #fefeef bold',
    Token.AcceptMessage:                                  'bg:#450039 #fee994',
    Token.ExitConfirmation:                               'bg:#fe8f94 #450000',
    Token.LineNumber:                                     'bg:#721d00 #cdd323',
    Token.SearchMatch:                                    'bg:#9f4b7d #fefeef',
    Token.SearchMatch.Current:                            'bg:#fe4b00 #fefeef',
    Token.SelectedText:                                   'bg:#cd787d #fefeef',
    Token.Toolbar.Completions:                            'bg:#450000 #feef00',
    Token.Toolbar.Completions.Arrow:                      'bg:#450000 #feef00 bold',
    Token.Toolbar.Completions.Completion:                 'bg:#450000 #feef00',
    Token.Toolbar.Completions.Completion.Current:         'bg:#fefeef #b17d00',
    Token.Menu.Completions.Completion:                    'bg:#450000 #fefe00',
    Token.Menu.Completions.Completion.Current:            'bg:#fefeef #b1fe00',
    Token.Menu.Completions.Meta:                          'bg:#450000 #cffe00',
    Token.Menu.Completions.Meta.Current:                  'bg:#450000 #edfe00',
    Token.Menu.Completions.ProgressBar:                   'bg:#edfeb5           ',
    Token.Menu.Completions.ProgressButton:                'bg:#454d00           ',
})
splicer1=temp

temp = {
    Token.LineNumber:                                     'bg:#720000 #cd23d3',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #00fa00 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #0045fe',
    Token.Out.Number:                                     '           #0045fe',
    Token.Separator:                                      '           #94fee9',
    Token.Toolbar.Search:                                 '           #7dfe1d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #7dfe1d noinherit',
    Token.Toolbar.Arg:                                    '           #7dfe1d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#94fe4b #004500',
    Token.Toolbar.Signature.CurrentName:                  'bg:#50fa00 #effefe bold',
    Token.Toolbar.Signature.Operator:                     '           #004500            bold',
    Token.Docstring:                                      '           #50faa5',
    Token.Toolbar.Validation:                             'bg:#00454b #7dfed3',
    Token.Toolbar.Status:                                 'bg:#00721d #7dfed3',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#00721d #00fe1d',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#00721d #0072d3',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#00721d #7dfefe',
    Token.Toolbar.Status.Key:                             'bg:#004500 #50faa5',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#009fd3 #effefe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#237278 #7dfed3',
    Token.Toolbar.Status.PythonVersion:                   'bg:#00721d #effefe bold',
    Token.Aborted:                                        '           #50faa5',
    Token.Sidebar:                                        'bg:#94fee9 #004500',
    Token.Sidebar.Title:                                  'bg:#effa78 #effefe bold',
    Token.Sidebar.Label:                                  'bg:#94fee9 #00721d',
    Token.Sidebar.Status:                                 'bg:#c1fefe #004500',
    Token.Sidebar.Selected.Label:                         'bg:#00721d #d8fefe',
    Token.Sidebar.Selected.Status:                        'bg:#009f4b #effefe bold',
    Token.Sidebar.Separator:                              'bg:#94fee9 #effefe underline',
    Token.Sidebar.Key:                                    'bg:#94fee9 #004500 bold',
    Token.Sidebar.Key.Description:                        'bg:#94fee9 #004500',
    Token.Sidebar.HelpText:                               'bg:#effefe #004500',
    Token.History.Line:                                   '',                        
    Token.History.Line.Selected:                          'bg:#00fa00 #004500',
    Token.History.Line.Current:                           'bg:#effefe #004500',
    Token.History.Line.Selected.Current:                  'bg:#50fea5 #004500',
    Token.History.ExistingInput:                          '           #50faa5',
    Token.Window.Border:                                  '           #944500',
    Token.Window.Title:                                   'bg:#94fee9 #004500',
    Token.Window.TIItleV2:                                'bg:#94fa78 #004500 bold',
    Token.AcceptMessage:                                  'bg:#50fefe #009f4b',
    Token.ExitConfirmation:                               'bg:#009fa5 #effefe',
}                                                                                                
temp.update({                                                                                                
    Token.Aborted:                                        '           #e3398f',                      
    Token.Sidebar:                                        'bg:#009f4b #effefe',
    Token.Sidebar.Title:                                  'bg:#00e3bc #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#009f4b #c1fefe',
    Token.Sidebar.Status:                                 'bg:#00721d #d8fefe',
    Token.Sidebar.Selected.Label:                         'bg:#c1fefe #005b07',
    Token.Sidebar.Selected.Status:                        'bg:#94fee9 #004500 bold',
    Token.Sidebar.Separator:                              'bg:#009f4b #004500 underline',
    Token.Sidebar.Key:                                    'bg:#00724b #effefe bold',
    Token.Sidebar.Key.Description:                        'bg:#009f4b #effefe',
    Token.Sidebar.HelpText:                               'bg:#005b07 #d8fefe',
    Token.History.Line:                                   '',                       
    Token.History.Line.Selected:                          'bg:#efe3fe #effefe',
    Token.History.Line.Current:                           'bg:#004500 #effefe',
    Token.History.Line.Selected.Current:                  'bg:#39458f #effefe',
    Token.History.ExistingInput:                          '           #39e38f',
    Token.Window.Border:                                  '           #00fefe',
    Token.Window.Title:                                   'bg:#009f4b #effefe',
    Token.Window.TIItleV2:                                'bg:#00e3bc #effefe bold',
    Token.AcceptMessage:                                  'bg:#394500 #94fee9',
    Token.ExitConfirmation:                               'bg:#94fe8f #004500',
    Token.LineNumber:                                     'bg:#00721d #23cdd3',
    Token.SearchMatch:                                    'bg:#7d9f4b #effefe',
    Token.SearchMatch.Current:                            'bg:#00fe4b #effefe',
    Token.SelectedText:                                   'bg:#7dcd78 #effefe',
    Token.Toolbar.Completions:                            'bg:#004500 #00feef',
    Token.Toolbar.Completions.Arrow:                      'bg:#004500 #00feef bold',
    Token.Toolbar.Completions.Completion:                 'bg:#004500 #00feef',
    Token.Toolbar.Completions.Completion.Current:         'bg:#effefe #00b17d',
    Token.Menu.Completions.Completion:                    'bg:#004500 #00fefe',
    Token.Menu.Completions.Completion.Current:            'bg:#effefe #00b1fe',
    Token.Menu.Completions.Meta:                          'bg:#004500 #00cffe',
    Token.Menu.Completions.Meta.Current:                  'bg:#004500 #00edfe',
    Token.Menu.Completions.ProgressBar:                   'bg:#b5edfe           ',
    Token.Menu.Completions.ProgressButton:                'bg:#00454d           ',
})
splicer2=temp



temp = {
    Token.LineNumber:                                     'bg:#007200 #23cdd3',
    Token.Prompt:                                         '                           bold',
    Token.Prompt.Dots:                                    '                   noinherit',
    Token.In:                                             '           #fa0000 bold',
    Token.In.Number:                                      '                        ',
    Token.Out:                                            '           #4500fe',
    Token.Out.Number:                                     '           #4500fe',
    Token.Separator:                                      '           #fe94e9',
    Token.Toolbar.Search:                                 '           #fe7d1d noinherit',
    Token.Toolbar.Search.Text:                            '                   noinherit',
    Token.Toolbar.System:                                 '           #fe7d1d noinherit',
    Token.Toolbar.Arg:                                    '           #fe7d1d noinherit',
    Token.Toolbar.Arg.Text:                               '                                 noinherit',
    Token.Toolbar.Signature:                              'bg:#fe944b #450000',
    Token.Toolbar.Signature.CurrentName:                  'bg:#fa5000 #feeffe bold',
    Token.Toolbar.Signature.Operator:                     '           #450000            bold',
    Token.Docstring:                                      '           #fa50a5',
    Token.Toolbar.Validation:                             'bg:#45004b #fe7dd3',
    Token.Toolbar.Status:                                 'bg:#72001d #fe7dd3',
    Token.Toolbar.Status.BatteryPluggedIn:                'bg:#72001d #fe001d',
    Token.Toolbar.Status.BatteryNotPluggedIn:             'bg:#72001d #7200d3',
    Token.Toolbar.Status.Title:                           '                   underline',
    Token.Toolbar.Status.InputMode:                       'bg:#72001d #fe7dfe',
    Token.Toolbar.Status.Key:                             'bg:#450000 #fa50a5',
    Token.Toolbar.Status.PasteModeOn:                     'bg:#9f00d3 #feeffe',
    Token.Toolbar.Status.PseudoTerminalCurrentVariable:   'bg:#722378 #fe7dd3',
    Token.Toolbar.Status.PythonVersion:                   'bg:#72001d #feeffe bold',
    Token.Aborted:                                        '           #fa50a5',
    Token.Sidebar:                                        'bg:#fe94e9 #450000',
    Token.Sidebar.Title:                                  'bg:#faef78 #feeffe bold',
    Token.Sidebar.Label:                                  'bg:#fe94e9 #72001d',
    Token.Sidebar.Status:                                 'bg:#fec1fe #450000',
    Token.Sidebar.Selected.Label:                         'bg:#72001d #fed8fe',
    Token.Sidebar.Selected.Status:                        'bg:#9f004b #feeffe bold',
    Token.Sidebar.Separator:                              'bg:#fe94e9 #feeffe underline',
    Token.Sidebar.Key:                                    'bg:#fe94e9 #450000 bold',
    Token.Sidebar.Key.Description:                        'bg:#fe94e9 #450000',
    Token.Sidebar.HelpText:                               'bg:#feeffe #450000',
    Token.History.Line:                                   '',                        
    Token.History.Line.Selected:                          'bg:#fa0000 #450000',
    Token.History.Line.Current:                           'bg:#feeffe #450000',
    Token.History.Line.Selected.Current:                  'bg:#fe50a5 #450000',
    Token.History.ExistingInput:                          '           #fa50a5',
    Token.Window.Border:                                  '           #459400',
    Token.Window.Title:                                   'bg:#fe94e9 #450000',
    Token.Window.TIItleV2:                                'bg:#fa9478 #450000 bold',
    Token.AcceptMessage:                                  'bg:#fe50fe #9f004b',
    Token.ExitConfirmation:                               'bg:#9f00a5 #feeffe',
}                                                                                                
temp.update({                                                                                                
    Token.Aborted:                                        '           #39e38f',                      
    Token.Sidebar:                                        'bg:#9f004b #feeffe',
    Token.Sidebar.Title:                                  'bg:#e300bc #ffffff bold',
    Token.Sidebar.Label:                                  'bg:#9f004b #fec1fe',
    Token.Sidebar.Status:                                 'bg:#72001d #fed8fe',
    Token.Sidebar.Selected.Label:                         'bg:#fec1fe #5b0007',
    Token.Sidebar.Selected.Status:                        'bg:#fe94e9 #450000 bold',
    Token.Sidebar.Separator:                              'bg:#9f004b #450000 underline',
    Token.Sidebar.Key:                                    'bg:#72004b #feeffe bold',
    Token.Sidebar.Key.Description:                        'bg:#9f004b #feeffe',
    Token.Sidebar.HelpText:                               'bg:#5b0007 #fed8fe',
    Token.History.Line:                                   '',                       
    Token.History.Line.Selected:                          'bg:#e3effe #feeffe',
    Token.History.Line.Current:                           'bg:#450000 #feeffe',
    Token.History.Line.Selected.Current:                  'bg:#45398f #feeffe',
    Token.History.ExistingInput:                          '           #e3398f',
    Token.Window.Border:                                  '           #fe00fe',
    Token.Window.Title:                                   'bg:#9f004b #feeffe',
    Token.Window.TIItleV2:                                'bg:#e300bc #feeffe bold',
    Token.AcceptMessage:                                  'bg:#453900 #fe94e9',
    Token.ExitConfirmation:                               'bg:#fe948f #450000',
    Token.LineNumber:                                     'bg:#72001d #cd23d3',
    Token.SearchMatch:                                    'bg:#9f7d4b #feeffe',
    Token.SearchMatch.Current:                            'bg:#fe004b #feeffe',
    Token.SelectedText:                                   'bg:#cd7d78 #feeffe',
    Token.Toolbar.Completions:                            'bg:#450000 #fe00ef',
    Token.Toolbar.Completions.Arrow:                      'bg:#450000 #fe00ef bold',
    Token.Toolbar.Completions.Completion:                 'bg:#450000 #fe00ef',
    Token.Toolbar.Completions.Completion.Current:         'bg:#feeffe #b1007d',
    Token.Menu.Completions.Completion:                    'bg:#450000 #fe00fe',
    Token.Menu.Completions.Completion.Current:            'bg:#feeffe #b100fe',
    Token.Menu.Completions.Meta:                          'bg:#450000 #cf00fe',
    Token.Menu.Completions.Meta.Current:                  'bg:#450000 #ed00fe',
    Token.Menu.Completions.ProgressBar:                   'bg:#edb5fe           ',
    Token.Menu.Completions.ProgressButton:                'bg:#45004d           ',
})
breeze=temp
