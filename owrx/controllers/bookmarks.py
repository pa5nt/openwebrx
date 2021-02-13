from owrx.controllers.template import WebpageController
from owrx.controllers.admin import AuthorizationMixin
from owrx.bookmarks import Bookmark, Bookmarks
from owrx.modes import Modes


class BookmarksController(AuthorizationMixin, WebpageController):
    def header_variables(self):
        variables = super().header_variables()
        variables["assets_prefix"] = "../"
        return variables

    def template_variables(self):
        variables = super().template_variables()
        variables["bookmarks"] = self.render_table()
        return variables

    def render_table(self):
        bookmarks = Bookmarks.getSharedInstance()

        def render_mode(m):
            return """
                <option value={mode}>{name}</option>
            """.format(
                mode=m.modulation,
                name=m.name,
            )

        return """
            <table class="table bookmarks">
                <tr>
                    <th>Name</th>
                    <th class="frequency">Frequency</th>
                    <th>Modulation</th>
                    <th>Actions</th>
                </tr>
                {bookmarks}
                <tr class="inputs" style="display:none;">
                    <td><input class="form-control form-control-sm" type="text" name="name"></td>
                    <td><input class="form-control form-control-sm" type="number" step="1" name="frequency"></td>
                    <td><select class="form-control form-control-sm" name="modulation">{options}</select></td>
                    <td></td>
                </tr>
            </table>
        """.format(
            bookmarks="".join(self.render_bookmark(idx, b) for idx, b in enumerate(bookmarks.getBookmarks())),
            options="".join(render_mode(m) for m in Modes.getAvailableModes()),
        )

    def render_bookmark(self, idx: int, bookmark: Bookmark):
        mode = Modes.findByModulation(bookmark.getModulation())
        return """
            <tr data-index="{index}" data-id="{id}">
                <td>{name}</td>
                <td class="frequency">{frequency}</td>
                <td data-value="{modulation}">{modulation_name}</td>
                <td>
                    <div class="btn btn-sm btn-danger bookmark-delete">delete</div>
                </td>
            </tr>
        """.format(
            index=idx,
            id=id(bookmark),
            name=bookmark.getName(),
            frequency=bookmark.getFrequency(),
            modulation=bookmark.getModulation() if mode is None else mode.modulation,
            modulation_name=bookmark.getModulation() if mode is None else mode.name,
        )

    def indexAction(self):
        self.serve_template("settings/bookmarks.html", **self.template_variables())