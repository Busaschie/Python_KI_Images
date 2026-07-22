1) Here is a reference image prompt: '__ref__'.
2) Generate a list of all criteria in the reference prompt.
3) Weight the listed criteria by their significance to achieve the expected image:
   - the total weight of all criteria must sum up to 1.
4) For each criteria, build a score as float number between 0 and 1, representing how much the image fulfills it:
   - while 0 means not fulfilled at all and 1 means entirely fulfilled.
5) Calculate the weighted mean of all those scores as a float number.
6) Only return this weighted mean, without adding any comments or metadata.