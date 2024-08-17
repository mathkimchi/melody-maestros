{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  # nativeBuildInputs is usually what you want -- tools you need to run
  nativeBuildInputs = with pkgs.buildPackages; [ 
    python3
  ];
  
  # from the nixos wiki's python page
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.numpy
      python-pkgs.matplotlib
      python-pkgs.pygame
      python-pkgs.pyaudio
      python-pkgs.aubio
      # python-pkgs.pandas
      # python-pkgs.requests
    ]))
  ];
}
