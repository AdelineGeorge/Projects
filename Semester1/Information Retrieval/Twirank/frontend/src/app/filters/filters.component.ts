import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormControl, FormArray } from '@angular/forms';
import { PushBasedService } from '../push-based.service';
import { SearchServiceService } from '../search-service.service';
import { CheckboxType } from '../search.interface';
import { Observable } from 'rxjs';
const POI_NAMES = ["CDCgov",
"VP" ,
"POTUS" ,
"GOPLeader" ,
"PressSec",
"MoHFW_INDIA" ,
"narendramodi" ,
"RahulGandhi" ,
"AmitShah" ,
"ArvindKejriwal" ,
"Lopezobrador" ,
"HLGatell" ,
"SaludEdomex" ,
"MarkoCortes" ,
"SSalud_mx" ,
"Irma_Sandoval" ,
"Claudiashein" ,
"LeaderMcConnell" ,
"myogiadityanath" ,
"INCIndia"];
const LANGUAGES = [
  "English",
  "Hindi",
  "Spanish"
];
const COUNTRIES = [
  "India",
  "Mexico",
  "USA"
];
const VERIFIED = [
  "true",
  "false"
];
@Component({
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.css']
})
export class FiltersComponent implements OnInit {
  poiNames: CheckboxType[] = [];
  languages: CheckboxType[] = [];
  countries: CheckboxType[] = [];
  verified: CheckboxType[] = [];
  form: FormGroup;
  queryVal$: Observable<string> = this.pushbased.queryVal$;
  
  constructor(private searchService: SearchServiceService,  private pushbased: PushBasedService) { }

  ngOnInit(): void {
    // bind props with data from database
    this.parseArrays();
    this.form = new FormGroup({
      poiNames: new FormArray([]),
      countries: new FormArray([]),
      languages: new FormArray([]),
      verified: new FormArray([])
    });
    // bind existing value to form control
    this._patchValues();
  }
  parseArrays() {
    for( var i of POI_NAMES) {
      let poinamesobj : CheckboxType = { name: '', checked: false};
      poinamesobj.name = i;
      poinamesobj.checked = false;
      this.poiNames.push(poinamesobj);

    }
    for( var i of LANGUAGES) {
      let languageobj : CheckboxType = { name: '', checked: false};
      languageobj.name = i;
      languageobj.checked = false;
      this.languages.push(languageobj);

    }
    for( var i of COUNTRIES) {
      let countryobj : CheckboxType = { name: '', checked: false};
      countryobj.name = i;
      countryobj.checked = false;
      this.countries.push(countryobj);

    }
    for( var i of VERIFIED) {
      let verifiedobj : CheckboxType = { name: '', checked: false};
      verifiedobj.name = i;
      verifiedobj.checked = false;
      this.verified.push(verifiedobj);

    }
  }
  click() {
    const formArray1 = this.form.get('countries') as FormArray;
    const formArray2 = this.form.get('languages') as FormArray;
    const formArray3 = this.form.get('poiNames') as FormArray;
    const formArray4 = this.form.get('verified') as FormArray;
    formArray1.patchValue(this.countries);
    formArray2.patchValue(this.languages);
    formArray3.patchValue(this.poiNames);
    formArray4.patchValue(this.verified);
    //this.form.reset();
  }
  private _patchValues() {
    // get array control
    const formArray1 = this.form.get('countries') as FormArray;
    // loop each existing value 
    this.countries.forEach(country => {
      formArray1.push(new FormGroup({
        name: new FormControl(country.name),
        checked: new FormControl(country.checked)
      }))
    })

    // get array control
    const formArray2 = this.form.get('languages') as FormArray;
    // loop each existing value 
    this.languages.forEach(language => {
      formArray2.push(new FormGroup({
        name: new FormControl(language.name),
        checked: new FormControl(language.checked)
      }))
    })

    // get array control
    const formArray3 = this.form.get('poiNames') as FormArray;
    // loop each existing value 
    this.poiNames.forEach(poiName => {
      formArray3.push(new FormGroup({
        name: new FormControl(poiName.name),
        checked: new FormControl(poiName.checked)
      }))
    })

    // get array control
    const formArray4 = this.form.get('verified') as FormArray;
    // loop each existing value 
    this.verified.forEach(verified => {
      formArray4.push(new FormGroup({
        name: new FormControl(verified.name),
        checked: new FormControl(verified.checked)
      }))
    })
  }

  submitForm() {
    const value = this.form.value;
    const selectedpoi = this.form.value.poiNames.filter(f => f.checked);
    const selectedlanguage = this.form.value.languages.filter(f => f.checked);
    const selectedcountry = this.form.value.countries.filter(f => f.checked);
    const selectedverified = this.form.value.verified.filter(f => f.checked);
    console.log('current form value: ', value);
    console.log('only selected form poi value: ', selectedpoi);
    console.log('only selected form selectedlanguage value: ', selectedlanguage);
    console.log('only selected form selectedcountry value: ', selectedcountry);
    console.log('only selected form selectedverified value: ', selectedverified); 
    const query = { "query" : '', "filters": {
      "languages": [],
      "country": [],
      "poi": [],
      "verified": []
    }}
    query.filters = this.parseFilterQuery(selectedpoi, selectedlanguage, selectedcountry, selectedverified)
    this.queryVal$.subscribe(data=> {
      query.query = data;
      this.pushbased.addQueryResults(query);
    })
    
  }
  parseFilterQuery(selectedpoi, selectedlanguage, selectedcountry, selectedverified) {
    // const query = { "query" : this.queryVal, "filters": {
    //   "languages": [],
    //   "country": [],
    //   "POI": [],
    //   "verified": []
    // }}
    const filters = {
      "languages": [],
      "country": [],
      "poi": [],
      "verified": []
    };
    if ( selectedpoi.length !== 0 ) {
      for ( var i of selectedpoi) {
        filters.poi.push(i.name);
      }
    }
    if ( selectedlanguage.length !== 0 ) {
      for ( var i of selectedlanguage) {
        filters.languages.push(i.name);
      }
    }
    if ( selectedcountry.length !== 0 ) {
      for ( var i of selectedcountry) {
        filters.country.push(i.name);
      }
    }
    if ( selectedverified.length !== 0 ) {
      for ( var i of selectedverified) {
        filters.verified.push(i.name);
      }
    }
    return filters;
  }

}
