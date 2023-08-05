
from vsg import rule

import re


class rule_011(rule.rule):
    '''Whitespace rule 011 checks for spaces before and after math operators.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'whitespace'
        self.identifier = '011'
        self.phase = 2
        self.solution = 'Add a single space before and/or after math operator.'

    def _analyze(self, oFile, oLine, iLineNumber):
        sLine = oLine.lineNoComment
        if not re.match('^.*".*/.*"', sLine):
            if re.match('^.*[\w+|\)][+|\-|/|*]', sLine) or re.match('^.*[+|\-|/|*][\w+|\(]', sLine):
                self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            iCommentIndex = oLine.line.find('--')
            if iCommentIndex == -1:
                oLine.update_line(re.sub(r'(\w+)([+|\-|/|*])', r'\1 \2', oLine.line))
                oLine.update_line(re.sub(r'\)([+|\-|/|*])', r') \1', oLine.line))
                oLine.update_line(re.sub(r'([+|\-|/|*])(\w+)', r'\1 \2', oLine.line))
                oLine.update_line(re.sub(r'([+|\-|/|*])\(', r'\1 (', oLine.line))
            else:
                sLine = oLine.line[:iCommentIndex]
                sLine = re.sub(r'(\w+)([+|\-|/|*])', r'\1 \2', sLine)
                sLine = re.sub(r'\)([+|\-|/|*])', r') \1', sLine)
                sLine = re.sub(r'([+|\-|/|*])(\w+)', r'\1 \2', sLine)
                sLine = re.sub(r'([+|\-|/|*])\(', r'\1 (', sLine)
                sLine = sLine + oLine.line[iCommentIndex:]
                oLine.update_line(sLine)
