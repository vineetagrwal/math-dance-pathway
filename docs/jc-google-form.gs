/**
 * One-click Google Form builder for the Jersey City POC.
 * Paste into https://script.google.com (New project), Save, Run, authorize.
 * Then open View -> Logs to get the LIVE form URL and Responses sheet URL.
 */
function createJCForm() {
  var form = FormApp.create('Jersey City - Report a School Math Contests');
  form.setDescription('Help map which Jersey City schools offer math competitions (AMC, MOEMS, MATHCOUNTS, Math League, Math Kangaroo). No account needed, takes 30 seconds.');

  form.addTextItem().setTitle('School name').setRequired(true);

  form.addCheckboxItem().setTitle('Which contests does this school host?')
      .setChoiceValues(['AMC 8', 'AMC 10', 'AMC 12', 'MOEMS', 'MATHCOUNTS', 'Math League', 'Math Kangaroo']);

  form.addTextItem().setTitle('Earliest grade students compete (optional)');

  form.addMultipleChoiceItem().setTitle('Did you just register this school as a NEW test site?')
      .setChoiceValues(['Yes - new site', 'No / not sure']);

  form.addParagraphTextItem().setTitle('Anything wrong or missing? (grades, type, contact, etc.)');

  form.addTextItem().setTitle('Your email (so we can confirm)').setRequired(true);

  form.addMultipleChoiceItem().setTitle('I am a:')
      .setChoiceValues(['Parent', 'Teacher / Staff', 'Student', 'Other']);

  var ss = SpreadsheetApp.create('Jersey City School Contests - Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('LIVE form URL: ' + form.getPublishedUrl());
  Logger.log('Responses sheet: ' + ss.getUrl());
  Logger.log('Edit form URL: ' + form.getEditUrl());
}
