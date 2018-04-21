import json


class SnapshotsFile:
    '''
    A file stored in the cloud repo describing the states of the project folder

    Example:
        {
          "host": "hostname",
          "hid": "Hc539ecf2a69ff89814c117dc8a7d43fa6c4ad83f",
          "alias": "my name",
          "paths": {
            "F1": "File 1.txt",
            "F2": "File 2.dat"
          },
          "file_versions": {
            "V1": {
              "path": "F1",
              "size": 30123456,
              "sha1": "e0996a37c13d44c3b06074939d43fa3759bd32c1"
            },
            "V2": {
              "path": "F2",
              "size": 30456789,
              "sha1": "c9c7c20935c621ce95b78623983574928c0c20c2"
            },
            "V3": {
              "path": "F2",
              "size": 30456789,
              "sha1": "c9c7c20935c621ce95b78623983574928c0c20c2"
            }
          },
          "snapshots": {
            "S1b6453892473a467d07372d45eb05abc2031647a": {
              "prior": [],
              "files": ["V1", "V2"],
              "summary": "First commit",
              "detail": null,
              "ts": "2012-04-23T18:25:43.511Z"
            },
            "Sb0f305140d965cc8bc02268c0a8127024b424ba6": {
              "prior": ["S1b6453892473a467d07372d45eb05abc2031647a"],
              "files": ["V1", "V3"],
              "summary": "Updated File 2.dat to be cool",
              "detail": null,
              "ts": "2012-04-23T18:25:43.511Z"
            }
          }
        }

    '''



