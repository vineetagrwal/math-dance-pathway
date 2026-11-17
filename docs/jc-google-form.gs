/**
 * One-click Google Form builder for the Jersey City POC.
 *
 * HOW TO USE (3 minutes):
 *  1. Go to https://script.google.com  ->  New project
 *  2. Delete the sample code, paste ALL of this, click Save.
 *  3. Click Run (the ▶ button). Google will ask you to authorize — allow it.
 *  4. Open View -> Logs (or the Execution log). It prints 3 links:
 *       - LIVE form URL   (share this / we link the Verify button to it)
 *       - Responses sheet (your live database)
 *       - Edit form URL
 *  5. Send me the LIVE form URL. Then in the Responses sheet:
 *       File -> Share -> Publish to web -> (the responses tab) -> CSV -> Publish,
 *       and send me that CSV link too.
 *  6. I wire the JC page so the Verify button opens this form, and the map
 *     overlays the published CSV live — submissions update the site automatically.
 */
function createJCForm() {
  var form = FormApp.create('Jersey City — Report a School\'s Math Contests');
  form.setDescription('Help map which Jersey City schools offer math competitions (AMC, MOEMS, MATHCOUNTS, Math League, Math Kangaroo). No account needed — takes 30 seconds.');

  form.addTextItem().setTitle('School name').setRequired(true);

  form.addCheckboxItem().setTitle('Which contests does this school host?')
      .setChoiceValues(['AMC 8', 'AMC 10', 'AMC 12', 'MOEMS', 'MATHCOUNTS', 'Math League', 'Math Kangaroo']);

  form.addTextItem().setTitle('Earliest grade students compete (optional)');

  form.addMultipleChoiceItem().setTitle('Did you just register this school as a NEW test site?')
      .setChoiceValues(['Yes — new site!', 'No / not sure']);

  form.addParagraphTextItem().setTitle('Anything wrong or missing? (grades, school type, contact, etc.)');

  form.addTextItem().setTitle('Your email (so we can confirm)').setRequired(true);

  form.addMultipleChoiceItem().setTitle('I am a…')
      .setChoiceValues(['Parent', 'Teacher / Staff', 'Student', 'Other']);

  // Create a linked responses spreadsheet (your live database).
  var ss = SpreadsheetApp.create('Jersey City School Contests — Responses');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('LIVE form URL (share this): ' + form.getPublishedUrl());
  Logger.log('Responses sheet: ' + ss.getUrl());
  Logger.log('Edit form URL: ' + form.getEditUrl());
}
