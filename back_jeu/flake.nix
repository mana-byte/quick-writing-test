{
  description = "DevWeb Back Jeu Development Environment";

  nixConfig = {
    extra-substituters = [
      "https://nix-community.cachix.org"
      "https://vrheadcache.cachix.org"
    ];
    extra-trusted-public-keys = [
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      "vrheadcache.cachix.org-1:v0XsYmHf9iA9ZtIsdc+Bjyqtzx6DO5f/fiXq2Lq+blA="
    ];
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };

      python = pkgs.python312;

      pythonWithPackages = python.withPackages (ps:
        with ps; [
          python-lsp-server
        ]);
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          pythonWithPackages
          black
          postgresql
        ];

        shellHook = ''
          if [ ! -d .venv ]; then
            echo "Creating virtualenv with ultralytics ..."
            ${python.interpreter} -m venv .venv
            source .venv/bin/activate
            pip install --upgrade pip
            pip install pytest fastapi
            pip install uvicorn
            pip install "fastapi[standard]"
            pip install "psycopg[binary,pool]"
            pip install sqlalchemy
            pip install psycopg2-binary
            pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-httpx
          else
            source .venv/bin/activate
          fi

          echo "Virtualenv activated. 'ultralytics' installed with."
        '';
      };
    });
}
