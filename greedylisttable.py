
from docutils import io, nodes, statemachine, utils
from docutils.utils import SystemMessagePropagation
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table

class GreedyListTable(Table):
    """
    The concept of the GreedyListTable is a list-table implementation that does
    not mind you having different numbers of cells in each row.  It simply
    finds the longest row and then extends the first or last cell of all
    shorter rows to span the number of columns required to catch up.

    This makes the table only marginally more flexible but that is enough to
    avoid using the full reStructuredText table syntax in some situations.
    """ 

    # The code below is an edit of the ListTable class in:
    #
    #   docutils.parsers.rst.directives.tables

    has_content = True

    option_spec = {'header-rows': directives.nonnegative_int,
                   'stub-columns': directives.nonnegative_int,
                   'widths': directives.positive_int_list,
                   'bias': directives.unchanged,
                   'class': directives.class_option,
                   'name': directives.unchanged}

    def run(self):

        if not self.content:
            error = self.state_machine.reporter.error(
                'The "%s" directive is empty; content required.' % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        self.bias = self.options.get('bias', 'right')
        if self.bias not in ['left', 'right']:
            error = self.state_machine.reporter.error(
                'Unable to recognise greedy-line-table bias "%s%. Expecting "left" or "right".' % self.bias,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        title, messages = self.make_title()
        node = nodes.Element()          # anonymous container for parsing
        self.state.nested_parse(self.content, self.content_offset, node)

        try:
            num_cols, col_widths = self.check_list_content(node)
            table_data = [[item.children for item in row_list[0]]
                          for row_list in node[0]]
            header_rows = self.options.get('header-rows', 0)
            stub_columns = self.options.get('stub-columns', 0)
        except SystemMessagePropagation, detail:
            return [detail.args[0]]
        table_node = self.build_table_from_list(table_data, num_cols, col_widths,
                                                header_rows, stub_columns)
        table_node['classes'] += self.options.get('class', [])
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def check_list_content(self, node):

        if len(node) != 1 or not isinstance(node[0], nodes.bullet_list):
            error = self.state_machine.reporter.error(
                'Error parsing content block for the "%s" directive: '
                'exactly one bullet list expected.' % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            raise SystemMessagePropagation(error)

        list_node = node[0]
        num_cols = 0

        # Check for a two-level bullet list and figure out the largest number
        # of columns in any row
        for item_index in range(len(list_node)):
            item = list_node[item_index]
            if len(item) != 1 or not isinstance(item[0], nodes.bullet_list):
                error = self.state_machine.reporter.error(
                    'Error parsing content block for the "%s" directive: '
                    'two-level bullet list expected, but row %s does not '
                    'contain a second-level bullet list.'
                    % (self.name, item_index + 1), nodes.literal_block(
                    self.block_text, self.block_text), line=self.lineno)
                raise SystemMessagePropagation(error)

            num_cols = max(len(item[0]), num_cols)

        col_widths = self.get_column_widths(num_cols)
        return num_cols, col_widths

    def get_column_widths(self, max_cols):
        if 'widths' in self.options:
            col_widths = self.options['widths']
            if len(col_widths) != max_cols:
                error = self.state_machine.reporter.error(
                    '"%s" widths do not match the number of columns in table '
                    '(%s).' % (self.name, max_cols), nodes.literal_block(
                    self.block_text, self.block_text), line=self.lineno)
                raise SystemMessagePropagation(error)
        elif max_cols:
            col_widths = [100 // max_cols] * max_cols
        return col_widths

    def build_table_from_list(self, table_data, num_cols, col_widths, header_rows, stub_columns):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(col_widths))
        table += tgroup
        for col_width in col_widths:
            colspec = nodes.colspec(colwidth=col_width)
            if stub_columns:
                colspec.attributes['stub'] = 1
                stub_columns -= 1
            tgroup += colspec
        rows = []
        for row in table_data:
            row_node = nodes.row()
            for cell_index, cell in enumerate(row):
                entry = nodes.entry()
                entry += cell
                row_node += entry
                if self.bias == "left" and not cell_index:
                    remainder = num_cols - len(row)
                    if remainder:
                        entry["morecols"] = remainder
                if self.bias == "right" and cell_index == len(row) - 1:
                    remainder = num_cols - (cell_index + 1)
                    if remainder:
                        entry["morecols"] = remainder
            rows.append(row_node)
        if header_rows:
            thead = nodes.thead()
            thead.extend(rows[:header_rows])
            tgroup += thead
        tbody = nodes.tbody()
        tbody.extend(rows[header_rows:])
        tgroup += tbody
        return table

def setup(app):

    app.add_directive('greedy-list-table', GreedyListTable)

