## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      <script type="text/javascript">

        var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};
        var dialog_opened = false;

        $(function() {

            $('#execute-results-button').click(function() {
                var count = $('.grid-wrapper').gridwrapper('results_count');
                if (!count) {
                    alert("There are no batch results to execute.");
                    return;
                }
                var form = $('form[name="execute-results"]');
                if (has_execution_options) {
                    $('#execution-options-dialog').dialog({
                        title: "Execution Options",
                        width: 550,
                        height: 300,
                        modal: true,
                        buttons: [
                            {
                                text: "Execute",
                                click: function(event) {
                                    dialog_button(event).button('option', 'label', "Executing, please wait...").button('disable');
                                    form.submit();
                                }
                            },
                            {
                                text: "Cancel",
                                click: function() {
                                    $(this).dialog('close');
                                }
                            }
                        ],
                        open: function() {
                            if (! dialog_opened) {
                                $('#execution-options-dialog select[auto-enhance="true"]').selectmenu();
                                $('#execution-options-dialog select[auto-enhance="true"]').on('selectmenuopen', function(event, ui) {
                                    show_all_options($(this));
                                });
                                dialog_opened = true;
                            }
                        }
                    });
                } else {
                    $(this).button('option', 'label', "Executing, please wait...").button('disable');
                    form.submit();
                }
            });

        });

      </script>
  % endif
  % endif
</%def>

<%def name="grid_tools()">
  ${parent.grid_tools()}
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      % if use_buefy:
          <b-button type="is-primary"
                    @click="executeResults()"
                    :disabled="!total">
            Execute Results
          </b-button>

          <b-modal has-modal-card
                   :active.sync="showExecutionOptions">
            <div class="modal-card">

              <header class="modal-card-head">
                <p class="modal-card-title">Execution Options</p>
              </header>

              <section class="modal-card-body">
                <p>
                  Please be advised, you are about to execute {{ total }} batches!
                </p>
                <br />
                <tailbone-form ref="executeResultsForm"></tailbone-form>
              </section>

              <footer class="modal-card-foot">
                <b-button @click="showExecutionOptions = false">
                  Cancel
                </b-button>
                <once-button type="is-primary"
                             @click="submitExecuteResults()"
                             text="Execute">
                </once-button>
              </footer>

            </div>
          </b-modal>

      % else:
          <button type="button" id="execute-results-button">Execute Results</button>
      % endif
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      <script type="text/javascript">

        TailboneForm.methods.submit = function() {
            this.$refs.actualForm.submit()
        }

        TailboneGridData.hasExecutionOptions = ${json.dumps(master.has_execution_options(batch))|n}
        TailboneGridData.showExecutionOptions = false

        TailboneGrid.methods.executeResults = function() {

            // this should never happen since we disable the button when there are no results
            if (!this.total) {
                alert("There are no batch results to execute.")
                return
            }

            if (this.hasExecutionOptions) {
                // show execution options modal, user can submit form from there
                this.showExecutionOptions = true

            } else {
                // no execution options, but this still warrants a basic confirmation
                if (confirm("Are you sure you wish to execute all " + this.total.toLocaleString('en') + " batches?")) {
                    alert('TODO: ok then you asked for it')
                }
            }
        }

        TailboneGrid.methods.submitExecuteResults = function() {
            this.$refs.executeResultsForm.submit()
        }

      </script>
  % endif
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      <script type="text/javascript">

        TailboneForm.data = function() { return TailboneFormData }

        Vue.component('tailbone-form', TailboneForm)

      </script>
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  % if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
      ${execute_form.render_deform(form_kwargs={'ref': 'actualForm'}, buttons=False)|n}
  % endif
</%def>


${parent.body()}

% if not use_buefy:
% if master.results_executable and request.has_perm('{}.execute_multiple'.format(permission_prefix)):
    <div id="execution-options-dialog" style="display: none;">
      <br />
      <p>
        Please be advised, you are about to execute multiple batches!
      </p>
      <br />
      ${execute_form.render_deform(form_kwargs={'name': 'execute-results'}, buttons=False)|n}
    </div>
% endif
% endif
